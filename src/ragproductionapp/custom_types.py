import pydantic

class RAGChunkAndSrc(pydantic.BaseModel):
    """
    A Pydantic model representing a chunk of text and its source.
    """
    chunks: list[str]
    source_id: str = None

class RAGUpsertResult(pydantic.BaseModel):
    """
    A Pydantic model representing the result of an upsert operation.
    """
    ingested: int

class RAGSearchResult(pydantic.BaseModel):
    """
    A Pydantic model representing the result of a search operation.
    """
    contexts: list[str]
    sources: list[str]

class RAGQueryResult(pydantic.BaseModel):
    """
    A Pydantic model representing the result of a query operation.
    """
    answer: str
    sources: list[str]
    num_contexts: int