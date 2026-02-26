from fastapi import HTTPException
from qdrant_client.models import Filter, FieldCondition, MatchAny
from app.services.embeddings import get_embedding
from app.config import qdrant_client, COLLECTION_NAME

def retrieve(query: str, user_role: str, k: int = 3):
    # --- generate embedding ---
    try:
        q_emb = get_embedding(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding failed: {str(e)}")

    # --- secure filter based on access_level ---
    query_filter = Filter(
        must=[
            FieldCondition(
                key="access_level",
                match=MatchAny(any=[user_role])
            )
        ]
    )

    # --- vector search ---
    try:
        results = qdrant_client.query_points(
            collection_name=COLLECTION_NAME,
            query=q_emb,
            limit=k,
            query_filter=query_filter,
            with_payload=True
        )
          
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vector search failed: {str(e)}")

    
    # --- return text safely ---
    return [
        point.payload.get("text", "")
        for point in results.points
        if point.payload
    ]

