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
        next_id = len(get_all_points(1000000))

        for vector, payload in zip(vectors, payloads):
            points.append(models.PointStruct(id=next_id, vector=vector, payload=payload))
            next_id += 1

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
    
def get_all_points(limit, collection_name = "data"):
    all_points = []
    offset = 0

    while True:
        response = client.scroll(
            collection_name=collection_name,
            limit=limit,
            with_payload=True,
            with_vectors=True,
            offset=offset
        )

        points = response[0]  # Первый элемент ответа - это список точек
        all_points.extend(points)
        
        if len(points) < limit:
            break

        offset += limit

    return all_points
    
    
vectors = [
        [0.1] * 128,
        [0.2] * 128,
        [0.3] * 128,
        [0.4] * 128,
        [0.5] * 128,
        [0.6] * 128,
    ]

payloads = [
        {"id": 1, "data": "Первая запись"},
        {"id": 2, "data": "Вторая запись"},
        {"id": 3, "data": "Третья запись"},
        {"id": 4, "data": "Третья запись"},
        {"id": 5, "data": "Третья запись"},
        {"id": 6, "data": "Третья запись"},
    ]

# Запрос к коллекции
#query_vector = [0.15] * 128
#search_result = get_from_collection(query_vector, 100)

#for hit in search_result:
    #print(f"ID: {hit.id}, Оценка: {hit.score}, Данные: {hit.payload}")



vectors = [
        [0.11] * 128,
        [0.21] * 128,
        [0.31] * 128,
        [0.41] * 128,
        [0.51] * 128,
        [0.61] * 128,
    ]

payloads = [
        {"id": 7, "data": "Первая запись"},
        {"id": 8, "data": "Вторая запись"},
        {"id": 9, "data": "Третья запись"},
        {"id": 10, "data": "Третья запись"},
        {"id": 11, "data": "Третья запись"},
        {"id": 12, "data": "Третья запись"},
    ]
print(add_to_collection(vectors, payloads))
print(len(get_all_points(1000)))

query_vector = [0.15] * 128
search_result = get_from_collection(query_vector, 100)

for hit in search_result:

    print(f"ID: {hit.id}, Оценка: {hit.score}, Данные: {hit.payload}")