from sentence_transformers import SentenceTransformer
import numpy as np

from typing import Literal

Model = Literal["paraphrase", "distiluse"]
MODEL = None
MODEL_TYPE = "paraphrase"

paraphrase = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
distiluse = SentenceTransformer("distiluse-base-multilingual-cased-v1")

def embed(sentence: str, model: Model) -> np.array:
    if type(MODEL) is None or MODEL_TYPE != model:
        match model:
            case "paraphrase":
                MODEL = paraphrase
            case "distiluse":
                MODEL = distiluse

    return MODEL.encode(sentence)

print(embed("Грету добивает телефонный звонок, где на том конце детский голос просит её соблюдать правила — у неё появляется подозрение, что дух Брамса вселился в куклу."))
