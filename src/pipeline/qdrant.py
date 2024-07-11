from qdrant_client import QdrantClient
from qdrant_client.http import models

client = QdrantClient(path="data.txt") 

def creating_collection(collection_name: str = "data"):
    try:
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=128, distance=models.Distance.COSINE)
        )
    except:
        raise Exception(f"Коллекция '{collection_name}' не создана.")
    
def add_to_collection():
    pass


def main():
    client = QdrantClient(path="data.txt") 

    # Создание коллекции
    collection_name = 'example_collection'
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=128, distance=models.Distance.COSINE)
    )

    print(f"Коллекция '{collection_name}' создана.")

    # Добавление данных в коллекцию
    vectors = [
        [0.1] * 128,
        [0.2] * 128,
        [0.3] * 128,
    ]

    payloads = [
        {"id": 1, "data": "Первая запись"},
        {"id": 2, "data": "Вторая запись"},
        {"id": 3, "data": "Третья запись"},
    ]

    points = []
    for i, (vector, payload) in enumerate(zip(vectors, payloads)):
        points.append(models.PointStruct(id=i, vector=vector, payload=payload))

    client.upsert(
        collection_name=collection_name,
        points=points
    )

    print(f"Добавлено {len(points)} точек в коллекцию '{collection_name}'.")

    # Запрос к коллекции
    query_vector = [0.15] * 128
    search_result = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=3
    )

    for hit in search_result:
        print(f"ID: {hit.id}, Оценка: {hit.score}, Данные: {hit.payload}")

if __name__ == "__main__":
    main()
