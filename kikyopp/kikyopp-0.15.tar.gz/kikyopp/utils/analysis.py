import requests

from kikyopp.utils.constants import YURI_API_HOST
from kikyopp.utils.retry import retry_rest_api


@retry_rest_api
def predict_bm_domain(content: str) -> list:
    resp = requests.post(
        f'{YURI_API_HOST}/bm-domain/api/predict-bm-domain',
        json={'text': content},
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json()['result']


@retry_rest_api
def extract_keywords(content: str) -> list:
    resp = requests.post(
        f'{YURI_API_HOST}/keywords/api/tag/keywords',
        json={'content': content},
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json()['keywords']


@retry_rest_api
def predict_themes(content: str) -> list:
    resp = requests.post(
        f'{YURI_API_HOST}/theme/api/tag/themes',
        json={'content': content},
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json()['result']
