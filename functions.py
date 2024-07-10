from nltk.tokenize import sent_tokenize
import spacy

def split_into_sentences(text, mode):
    """Разделяет текст на предложения по разным принципам"""
    if mode == "points":
        sentences = text.split(".")
    elif mode == "lines":
        sentences = text.split("\n")
    elif mode == "spaCy":
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)  
        sentences = [sent.text for sent in doc.sents]
    elif mode == "nltk":
        sentences = sent_tokenize(text)
    else:
        sentences =  "Выберете доступный режим: points, lines, spaCy, nltk"
    return sentences

#text = "Вы можете использовать любую модель для распознавания из списка.\n Для примера, воспользуемся моделью page, которая позволяет распознавать любое количество текста на изображении." # your text
#print(split_into_sentences(text, "lines"))
"""
from sentence_transformers import SentenceTransformer
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt
from nltk.tokenize import sent_tokenize

def generate_embeddings(sentences):
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    embeddings = model.encode(sentences)
    return embeddings

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


text = ""

sentences = split_into_sentences(text)

embeddings = generate_embeddings(sentences)
build_semantic_tree(embeddings)
"""


