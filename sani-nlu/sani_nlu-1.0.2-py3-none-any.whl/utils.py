import os
import gdown

from typing import Any, Dict
from sani_nlu.constants import MODEL_DIR, MODEL_NAME, BASE_URL

def initializeFolder():
	if not os.path.exists(MODEL_DIR):
		os.mkdir(MODEL_DIR)
		print("Directory ", MODEL_DIR," created")

def download_model():
    model_path = MODEL_DIR + MODEL_NAME

    if os.path.isfile(model_path) != True:
        print(f"{MODEL_NAME} will be downloaded...")
        gdown.download(BASE_URL + MODEL_NAME, model_path, quiet=False)

    return model_path

def is_duplicated(e1: Dict, e2: Dict):
    """
    check if 2 entities are shared the same index
    """
    return e1['start'] == e2['start'] and e1['end'] == e2['end']


def is_overlap(e1: Dict, e2: Dict):
    """
    check if 2 entities are overlapping in text index
    """
    return e1['start'] <= e2['start'] <= e1['end'] or e2['start'] <= e1['start'] <= e2['end']