import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct,
    ScoredPoint,
    Filter,
    FieldCondition,
    MatchValue,
)

import uuid
from typing import List, Dict

QDRANT_DB_PATH = "vector_db"
CLIENT = QdrantClient(path=QDRANT_DB_PATH)


def create_collection(size=128, collection: str = "default") -> None:
    CLIENT.recreate_collection(
        collection_name=collection,
        vectors_config=VectorParams(size=size, distance=Distance.COSINE),
    )


def insert(embeds, collection: str = "default") -> None:
    points = []

    for vector, payload in embeds:
        points.append(PointStruct(id=str(uuid.uuid4()), vector=vector, payload=payload))

    CLIENT.upsert(collection_name=collection, points=points)


def search(
    query: np.array, limit: int = 10, collection: str = "default", document: int = None
) -> List[ScoredPoint]:
    if document is None:
        filter = None
    else:
        filter = Filter(
            must=[FieldCondition(key="document", match=MatchValue(value=document))]
        )

    return CLIENT.search(
        collection_name=collection,
        query_vector=query,
        limit=limit,
        query_filter=filter,
    )


def convert_points(points: List[ScoredPoint]) -> List[Dict]:
    """Convert a list of points to a list of dicts"""
    out = []

    for point in points:
        out.append({"score": point.score, "payload": point.payload})

    return out
