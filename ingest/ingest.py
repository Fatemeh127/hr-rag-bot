import os, uuid, time, requests
from datetime import datetime, timezone

from qdrant_client import QdrantClient
from ingest.loaders.pdf_loader import load_pdf
from ingest.loaders.docx_loader import load_docx
from ingest.chunker import chunk_text

from app.services.embeddings import get_embedding
from app.config import qdrant_client, COLLECTION_NAME, QDRANT_URL

DATA_DIR = "data/hr_docs"

# wait for Qdrant run in docker
def wait_for_qdrant(url: str, retries=20, delay=2):
    for i in range(retries):
        try:
            r = requests.get(f"{url}/readyz", timeout=2)
            if r.status_code == 200:
                print("Qdrant is ready")
                return
        except Exception:
            pass

        print(f"Waiting for Qdrant... ({i+1}/{retries})")
        time.sleep(delay)

    raise RuntimeError("Qdrant not available after waiting")


def load_file(path: str) -> str:
    if path.endswith(".pdf"):
        return load_pdf(path)
    elif path.endswith(".docx"):
        return load_docx(path)
    else:
        raise ValueError(f"Unsupported file type: {path}")


def ingest():
    wait_for_qdrant(QDRANT_URL)

    qdrant_client = QdrantClient(url=QDRANT_URL)

    points = []

    for filename in os.listdir(DATA_DIR):
        file_path = os.path.join(DATA_DIR, filename)
        print(f"Processing {filename}...")

        text = load_file(file_path)
        chunks = chunk_text(text)

        for i, chunk in enumerate(chunks):
            points.append({
                "id": str(uuid.uuid4()),
                "vector": get_embedding(chunk),
                "payload": {
                    "text": chunk,
                    "doc_id": filename.rsplit(".", 1)[0],
                    "doc_type": "policy",
                    "department": "HR",
                    "source": filename,
                    "chunk_index": i,
                    "language": "en",
                    "created_at": datetime.now(timezone.utc).isoformat()
                }
            })

    if not points:
        print("No documents found to ingest.")
        return

    qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print(f"Ingest complete. Total chunks: {len(points)}")


ingest()