import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient

# ---------- Load environment variables ----------
load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL", "http://qdrant:6333")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "hr_docs")

# ---------- Qdrant client ----------
qdrant_client = QdrantClient(url=QDRANT_URL)

DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
