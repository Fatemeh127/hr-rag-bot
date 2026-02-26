import os, uuid, json, time, requests
from datetime import datetime, timezone
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from ingest.loaders.pdf_loader import load_pdf
from ingest.loaders.docx_loader import load_docx
from ingest.chunker import chunk_text
from app.services.embeddings import get_embedding
from app.config import qdrant_client, COLLECTION_NAME, QDRANT_URL

DATA_DIR = "data/hr_docs"
METADATA_FILE = os.path.join(DATA_DIR, "metadata.json")

# --- wait for Qdrant ---
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


# --- load file content ---
def load_file(path: str) -> str:
    if path.endswith(".pdf"):
        return load_pdf(path)
    elif path.endswith(".docx"):
        return load_docx(path)
    else:
        raise ValueError(f"Unsupported file type: {path}")


# --- ingest documents ---
def ingest():
    wait_for_qdrant(QDRANT_URL)

    # --- load metadata ---
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        metadata_mapping = json.load(f)

    points = []

    for doc_id, meta in metadata_mapping.items():
        file_path = os.path.join(DATA_DIR, meta["file_path"])
        text = load_file(file_path)
        chunks = chunk_text(text)
        created_at = datetime.now(timezone.utc).isoformat()

        for i, chunk in enumerate(chunks):
            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=get_embedding(chunk),
                    payload={
                        "text": chunk,
                        "doc_id": doc_id,
                        "doc_type": meta["doc_type"],
                        "access_level": meta["access_level"],
                        "department": meta["department"],
                        "source": meta["file_path"],
                        "chunk_index": i,
                        "language": "en",
                        "created_at": created_at
                    }
                )
            )

    # --- batch upsert برای performance ---
    qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print(f"Ingest complete. Total chunks: {len(points)}")


ingest()
