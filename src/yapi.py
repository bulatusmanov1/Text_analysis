"""
Yandex Cloud API shims
"""

import requests
import numpy as np

import os
from datetime import datetime, timedelta
from typing import Optional

FOLDER_ID = os.environ["FOLDER_ID"]
OAUTH_TOKEN = os.environ["OAUTH_TOKEN"]
__IAM_TIME = datetime(year=2000, month=1, day=1)
__IAM_TOKEN = ""

# constants
IAM_URL = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
EMBEDDING_URL = "https://llm.api.cloud.yandex.net:443/foundationModels/v1/textEmbedding"
COMPLETION_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

# derived constants
DOC_URI = f"emb://{FOLDER_ID}/text-search-doc/latest"
QUERY_URI = f"emb://{FOLDER_ID}/text-search-query/latest"
GPTPRO_URI = f"gpt://{FOLDER_ID}/yandexgpt/latest"
GPTLITE_URI = f"gpt://{FOLDER_ID}/yandexgpt-lite/latest"
SUMMARY_URI = f"gpt://{FOLDER_ID}/summarization/latest"


def iam_token() -> str:
    if datetime.now() - __IAM_TIME < timedelta(hours=1):
        return __IAM_TOKEN

    payload = {"yandexPassportOauthToken": OAUTH_TOKEN}
    r = requests.post(IAM_URL, json=payload)
    r.raise_for_status()

    return r.json()["iamToken"]


def headers():
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {iam_token()}",
        "x-folder-id": f"{FOLDER_ID}",
    }


def embedding(text: str, model: str = "doc") -> np.ndarray:
    payload = {
        "modelUri": DOC_URI if model == "doc" else QUERY_URI,
        "text": text,
    }

    r = requests.post(EMBEDDING_URL, json=payload, headers=headers())
    r.raise_for_status()

    return np.array(r.json()["embedding"])


def complete(
    query: str,
    instruction: Optional[str] = None,
    temperature: float = 0.1,
    max_tokens: int = 1000,
    model: str = "lite",
) -> str:
    uri = ""
    match model:
        case "pro":
            uri = GPTPRO_URI
        case "lite":
            uri = GPTLITE_URI
        case "summary":
            uri = SUMMARY_URI

    messages = [{"role": "user", "text": query}]
    if instruction is not None:
        messages.insert(0, {"role": "system", "text": instruction})

    payload = {
        "modelUri": uri,
        "completionOptions": {
            "stream": False,
            "temperature": temperature,
            "maxTokens": max_tokens,
        },
        "messages": messages,
    }

    r = requests.post(COMPLETION_URL, json=payload, headers=headers())

    text = r.json()["result"]["alternatives"][0]["message"]["text"]

    return text
