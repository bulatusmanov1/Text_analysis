"""
Yandex Cloud API shims
"""

import requests

import os
import json
from datetime import datetime, timedelta

FOLDER_ID = os.environ["FOLDER_ID"]
OAUTH_TOKEN = os.environ["OAUTH_TOKEN"]
__IAM_TIME = datetime(year=2000, month=1, day=1)
__IAM_TOKEN = ""

def iam_token():
    if datetime.now() - __IAM_TIME < timedelta(hours=1):
        return __IAM_TOKEN

    payload = {"yandexPassportOauthToken": OAUTH_TOKEN}
    r = requests.post(
        "https://iam.api.cloud.yandex.net/iam/v1/tokens",
        data=json.dumps(payload),
    )
    r.raise_for_status()

    return r["iam_token"]
