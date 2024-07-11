from qdrant_client import QdrantClient
from qdrant_client.http import models

client = QdrantClient(path="data.db") 

def creating_collection(size = 128, collection_name: str = "data"):
    try:
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=size, distance=models.Distance.COSINE)
        )
        return f"Коллекция '{collection_name}' создана."
    except:
        raise Exception(f"Коллекция '{collection_name}' не создана.")
    
def add_to_collection(vectors, payloads, collection_name = "data"):
    try:
        points = []
        for i, (vector, payload) in enumerate(zip(vectors, payloads)):
            points.append(models.PointStruct(id=i, vector=vector, payload=payload))

        client.upsert(
            collection_name=collection_name,
            points=points
        )
        return f"Добавление в коллекцию '{collection_name}' успешно."
    except:
        raise Exception(f"Добавление в коллекцию '{collection_name}' провалилось.")

def get_from_collection(query_vector, limit = 3, collection_name = "data"):
    try:
        search_result = client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit
        )
        return search_result
    except:
        raise Exception(f"Запрос к коллекции '{collection_name}' провалился.")