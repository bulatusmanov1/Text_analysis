import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct, ScoredPoint

import uuid
from typing import List

QDRANT_DB_PATH = "/vector_db"
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
    query: np.array, limit: int = 3, collection: str = "default"
) -> List[ScoredPoint]:
    return CLIENT.search(collection_name=collection, query_vector=query, limit=limit)
