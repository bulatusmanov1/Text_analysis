from sentence_transformers import SentenceTransformer
import numpy as np

from typing import Literal

Model = Literal["paraphrase", "distiluse"]

paraphrase = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
distiluse = SentenceTransformer("distiluse-base-multilingual-cased-v1")


def embed(sentence: str, model: Model) -> np.array:
    match model:
        case "paraphrase":
            model = paraphrase
        case "distiluse":
            model = distiluse

    return model.encode(sentence)
