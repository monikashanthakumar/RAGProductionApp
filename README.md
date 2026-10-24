# RAGProductionApp

A PDF question-answering application built around retrieval-augmented generation (RAG). Upload a PDF through the Streamlit interface, retrieve relevant text chunks from Qdrant, and generate answers grounded in those chunks using the Gemini API.

## How it works

1. The Streamlit app saves an uploaded PDF locally and sends an `rag/ingest_pdf` event to Inngest.
2. An Inngest function extracts text from the PDF, splits it into overlapping chunks, creates Gemini embeddings, and stores the chunks and source names in Qdrant.
3. When you ask a question, the app sends an `rag/query_pdf_ai` event.
4. An Inngest function embeds the question, retrieves the most relevant chunks from Qdrant, and asks Gemini to answer using that context. The app displays the answer and its source documents.

## Requirements

- Python 3.13 or later
- [uv](https://docs.astral.sh/uv/) for Python environment and package management
- [Docker](https://docs.docker.com/get-docker/) for running Qdrant
- Node.js and npm/npx for the local Inngest development server
- A Google Gemini API key with access to Gemini embeddings and the configured Gemini model

## Setup

Clone the repository, then install the project dependencies:

```bash
uv sync
```

Create a `.env` file in the repository root:

```dotenv
GEMINI_API_KEY=your_gemini_api_key
# Optional; defaults to http://127.0.0.1:8288/v1
INNGEST_API_BASE=http://127.0.0.1:8288/v1
```

The API base variable is used by the Streamlit app to poll Inngest for completed query results. The Inngest client and API server are configured for local development.

## Run locally

Start Qdrant in a terminal:

```bash
docker run --name rag-qdrant \
  -p 6333:6333 \
  -p 6334:6334 \
  -v "$(pwd)/qdrant_storage:/qdrant/storage" \
  qdrant/qdrant
```

The application connects to Qdrant at `http://localhost:6333` and uses the `docs` collection. The volume mount keeps the vector database data in the local, git-ignored `qdrant_storage/` directory.

Start the FastAPI app in another terminal:

```bash
uv run uvicorn ragproductionapp.main:app --reload
```

The Inngest functions are served by the FastAPI app at `/api/inngest`. Start the Inngest development server in a third terminal and point it at that endpoint:

```bash
npx inngest-cli@latest dev -u http://127.0.0.1:8000/api/inngest
```

Finally, launch the Streamlit interface:

```bash
uv run streamlit run src/ragproductionapp/streamlit_app.py
```

Open the URL printed by Streamlit (usually `http://localhost:8501`). Upload a PDF, then check the Inngest development UI at `http://localhost:8288` and wait for the ingestion function to complete before asking questions about it. The Streamlit interface confirms that ingestion was triggered; it does not wait for ingestion to finish. You can use [`src/data/sample.pdf`](src/data/sample.pdf) as an example document.

## Configuration

| Variable | Required | Default | Purpose |
| --- | --- | --- | --- |
| `GEMINI_API_KEY` | Yes | — | Authenticates Gemini embeddings and answer generation. |
| `INNGEST_API_BASE` | No | `http://127.0.0.1:8288/v1` | Inngest API base used by the UI when looking up query run results. |

The Qdrant URL (`http://localhost:6333`), collection (`docs`), embedding model (`gemini-embedding-001`), and vector dimension (`3072`) are currently configured in the application code.

## Project structure

```text
src/
├── data/
│   └── sample.pdf
└── ragproductionapp/
    ├── data_loader.py      # PDF extraction, text chunking, and Gemini embeddings
    ├── main.py             # FastAPI app and Inngest ingestion/query functions
    ├── streamlit_app.py    # PDF upload and question-answering UI
    ├── vector_db.py        # Qdrant collection, upsert, and search operations
    └── custom_types.py     # Data models used by the RAG workflow
```

Uploaded files are saved under `uploads/` in the current working directory. Keep private documents and generated uploads out of version control.

## Notes

- The answer-generation function uses the Gemini model configured in `src/ragproductionapp/main.py` through Gemini's OpenAI-compatible API endpoint.
- The query UI waits for the Inngest run output, with a five-minute timeout.
- The `ragproductionapp` command-line entry point is currently a placeholder; use the Uvicorn and Streamlit commands above to run the application.
