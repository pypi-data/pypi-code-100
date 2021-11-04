import requests


def create_model(model_id, model_name, org):
    body = {
        "model_id": model_id,
        "model_name": model_name,
        "organization": org
    }
    response = requests.post("https://mltrics.ai/api/v1/models", json=body)
    response.raise_for_status()
    return response.json()


def get_models(org):
    params = {"organization": org}
    response = requests.get("https://mltrics.ai/api/v1/models", params=params)
    response.raise_for_status()
    return response.json()


def upload_model_predictions(model_id, org, predictions):
    params = {
        "organization": org,
    }
    body = {
        "predictions": predictions,
    }
    response = requests.post(f"https://mltrics.ai/api/v1/models/{model_id}",
                             json=body,
                             params=params)
    response.raise_for_status()
    return response.json()


def get_model_predictions(model_id, org):
    params = {"organization": org}
    response = requests.get(
        f"https://mltrics.ai/api/v1/models/{model_id}/predictions",
        params=params)
    response.raise_for_status()
    return response.json()['predictions']


def compare_model_predictions(model_1, model_2, org):
    params = {"organization": org}
    response = requests.get(
        f"https://mltrics.ai/api/v1/models/compare/{model_1}/{model_2}",
        params=params)
    response.raise_for_status()
    return response.json()['results']
