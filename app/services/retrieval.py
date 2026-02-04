from app.services.embeddings import get_embedding
from app.config import qdrant_client, COLLECTION_NAME
from fastapi import HTTPException
from qdrant_client.models import Filter, FieldCondition, MatchValue

def retrieve(query: str, role: str, k: int = 3):
    q_emb = get_embedding(query)

    if role == "employee":
        query_filter = Filter(
            must=[
                FieldCondition(
                    key="doc_type",
                    match=MatchValue(value="policy")
                ),
                
                FieldCondition(
                    key="department",
                    match=MatchValue(value="HR")
                )
                
            ],
            must_not=[
                FieldCondition(
                    key ="doc_type",
                    match=MatchValue(value="contract")
                )
            ]
        )    
    elif role == "manager":
        query_filter = Filter(
            must=[
                FieldCondition(
                    key="department",
                    match=MatchValue(value="HR")
                )
            ],
            should=[
                FieldCondition(
                    key="doc_type",
                    match=MatchValue(value="policy")
                ),
                FieldCondition(
                    key="doc_type",
                    match=MatchValue(value="contract")
                )
            ]
        )
    elif role == "admin":
        query_filter = None

    else:
        raise HTTPException(
            status_code=403,
            detail="Role not allowed"
        )

    results = qdrant_client.query_points(
        collection_name= COLLECTION_NAME,
        query=q_emb,
        limit=k,
        query_filter= query_filter,
        with_payload=True
    )

    return [
    point.payload.get("text", "")
    for point in results.points
    if point.payload
]
