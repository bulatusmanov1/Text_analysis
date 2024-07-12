"""
Yandex Cloud foundation models API wrappers.
"""

import requests
import numpy as np

import os
import base64
from datetime import datetime, timedelta
from typing import Optional, List, Dict

FOLDER_ID = os.environ["FOLDER_ID"]
OAUTH_TOKEN = os.environ["OAUTH_TOKEN"]
__IAM_TIME = datetime(year=2000, month=1, day=1)
__IAM_TOKEN = ""

# constants
IAM_URL = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
EMBEDDING_URL = "https://llm.api.cloud.yandex.net:443/foundationModels/v1/textEmbedding"
COMPLETION_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
TOKENIZE_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/tokenize"
OCR_URL = "https://ocr.api.cloud.yandex.net/ocr/v1/recognizeText"

# derived constants
DOC_URI = f"emb://{FOLDER_ID}/text-search-doc/latest"
QUERY_URI = f"emb://{FOLDER_ID}/text-search-query/latest"
GPTPRO_URI = f"gpt://{FOLDER_ID}/yandexgpt/latest"
GPTLITE_URI = f"gpt://{FOLDER_ID}/yandexgpt-lite/latest"
SUMMARY_URI = f"gpt://{FOLDER_ID}/summarization/latest"


def _iam_token() -> str:
    if datetime.now() - __IAM_TIME < timedelta(hours=1):
        return __IAM_TOKEN

    payload = {"yandexPassportOauthToken": OAUTH_TOKEN}
    r = requests.post(IAM_URL, json=payload)
    r.raise_for_status()

    return r.json()["iamToken"]


def _headers():
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {_iam_token()}",
        "x-folder-id": f"{FOLDER_ID}",
    }


def embedding(text: str, model: str = "doc") -> np.array:
    """
    Get embedding of a string and return it as a 256-element NumPy array

    Keyword arguments:
    text -- text to embed
    model -- "doc" for document embedding and "query" for search embedding
    """
    payload = {
        "modelUri": DOC_URI if model == "doc" else QUERY_URI,
        "text": text,
    }

    r = requests.post(EMBEDDING_URL, json=payload, headers=_headers())
    r.raise_for_status()

    return np.array(r.json()["embedding"])


def _model_uri(model: str) -> str:
    match model:
        case "pro":
            return GPTPRO_URI
        case "lite":
            return GPTLITE_URI
        case "summary":
            return SUMMARY_URI


def complete(
    query: str,
    instruction: Optional[str] = None,
    temperature: float = 0.1,
    max_tokens: int = 1000,
    model: str = "lite",
) -> str:
    """
    Complete a query using a Yandex Foundation Model and return the answer

    Keyword arguments:
    query -- the input query, which has the user role (aka context)
    instruction -- if it's passed, the model will get a system-role command
    temperature -- must be in range 0-1, determines the model's randomness
    max_tokens -- limits the amout of tokens the model will output
    model -- "lite", "pro", or "summary"
    """
    messages = [{"role": "user", "text": query}]
    if instruction is not None:
        messages.insert(0, {"role": "system", "text": instruction})

    payload = {
        "modelUri": _model_uri(model),
        "completionOptions": {
            "stream": False,
            "temperature": temperature,
            "maxTokens": max_tokens,
        },
        "messages": messages,
    }

    r = requests.post(COMPLETION_URL, json=payload, headers=_headers())

    text = r.json()["result"]["alternatives"][0]["message"]["text"]

    return text


def tokenize(text: str, model: str = "lite") -> List[Dict]:
    """
    Returns tokenized text for a given model

    Keyword arguments:
    text -- text to tokenize
    model -- "lite", "pro", or "summary"
    """
    payload = {
        "modelUri": _model_uri(model),
        "text": text,
    }

    r = requests.post(TOKENIZE_URL, json=payload, headers=_headers())

    return r.json()["tokens"]


def ocr(pdf: bytes):
    content = base64.b64encode(pdf).decode("ascii")

    payload = {
        "mimeType": "application/pdf",
        "languageCodes": ["ru", "en"],
        "model": "page",
        "content": content,
    }

    r = requests.post(OCR_URL, json=payload, headers=_headers())

    return r.json()
