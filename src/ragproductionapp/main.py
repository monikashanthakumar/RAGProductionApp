import logging
from fastapi import FastAPI
import inngest
import inngest.fast_api
from inngest.experimental import ai
from dotenv import load_dotenv
import uuid
import os
import datetime

load_dotenv()  # Load environment variables from .env file

inggest_client = inngest.Inngest(
    app_id = "rag_app",
    logging = logging.getLogger("uvicorn"),
    is_production = False,
    serializer = inngest.PydanticSerializer
)

app = FastAPI()
