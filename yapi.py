"""
Yandex Cloud API shims
"""

import requests
import numpy as np

import os
import json
from datetime import datetime, timedelta

FOLDER_ID = os.environ["FOLDER_ID"]
OAUTH_TOKEN = os.environ["OAUTH_TOKEN"]
__IAM_TIME = datetime(year=2000, month=1, day=1)
__IAM_TOKEN = ""

# constants
IAM_URL = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
EMBEDDING_URL = "https://llm.api.cloud.yandex.net:443/foundationModels/v1/textEmbedding"

# derived constants
DOC_URI = f"emb://{FOLDER_ID}/text-search-doc/latest"
QUERY_URI = f"emb://{FOLDER_ID}/text-search-query/latest"


def iam_token():
    if datetime.now() - __IAM_TIME < timedelta(hours=1):
        return __IAM_TOKEN

    payload = {"yandexPassportOauthToken": OAUTH_TOKEN}
    r = requests.post(IAM_URL, json=payload)
    r.raise_for_status()

    return r["iam_token"]

def embedding(text: str, model: str = "doc"):

    payload = {
        "modelUri": DOC_URI if model == "doc" else QUERY_URI,
        "text": text,
    }

    r = requests.post(EMBEDDING_URL, json=payload)
    r.raise_for_status()

    return np.array(r["embedding"])
