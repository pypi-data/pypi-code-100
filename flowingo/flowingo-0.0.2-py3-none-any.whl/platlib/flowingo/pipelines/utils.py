import hashlib
import json
from typing import Any, Dict, List

HASH_LEN = 32


def get_pipeline_hash(pipeline: Dict[str, Any]) -> str:
    pipeline_tasks = pipeline
    json_dump = json.dumps(pipeline_tasks, sort_keys=True).encode('utf-8')
    return hashlib.md5(json_dump).hexdigest()[:HASH_LEN]


def get_pipeline_tasks_hash(pipeline_tasks: List[Dict[str, Any]]) -> str:
    json_dump = json.dumps(pipeline_tasks, sort_keys=True).encode('utf-8')
    return hashlib.md5(json_dump).hexdigest()[:HASH_LEN]
