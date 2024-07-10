from sentence_transformers import SentenceTransformer
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt
import numpy as np

# Шаг 1: Генерация эмбеддингов
def generate_embeddings(sentences):
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    embeddings = model.encode(sentences)
    return embeddings

# Шаг 2: Построение семантического дерева с использованием иерархической кластеризации
def build_semantic_tree(embeddings):
    # Выполнение иерархической кластеризации
    linked = linkage(embeddings, 'ward')
    print(linked)

    # Построение дендрограммы
    plt.figure(figsize=(10, 7))
    dendrogram(linked,
               orientation='top',
               distance_sort='descending',
               show_leaf_counts=True)
    plt.show()

# Пример использования
sentences = [
    "Привет, как дела?",
    "Это тестовое предложение.",
    "Сегодня хорошая погода.",
    "Я люблю программировать.",
    "Мы идем на прогулку."
]

embeddings = generate_embeddings(sentences)
build_semantic_tree(embeddings)

