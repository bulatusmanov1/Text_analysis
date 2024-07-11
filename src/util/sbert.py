from sentence_transformers import SentenceTransformer
import numpy as np

from typing import Literal

type Model = Literal["paraphrase", "distiluse"]
MODEL = None
MODEL_TYPE = "paraphrase"

def _model(model: Model) -> SentenceTransformer:
    match model:
        case "paraphrase":
            return SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
        case "distiluse":
            return SentenceTransformer("distiluse-base-multilingual-cased-v1")


def embed(sentence: str, model: Model) -> np.array:
    # don't recreate the model from scratch for each sentence
    if type(MODEL) is None or MODEL_TYPE != model:
        MODEL = _model(model)

    return MODEL.encode(sentence)
