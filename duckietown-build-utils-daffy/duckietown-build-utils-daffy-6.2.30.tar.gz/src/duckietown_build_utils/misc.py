import os
from typing import Dict, List

from duckietown_docker_utils import ENV_REGISTRY, IMPORTANT_ENVS

__all__ = ["get_important_env_build_args_dict", "get_important_env_build_args"]


def get_important_env_build_args_dict(dockerfile_content: str) -> Dict[str, str]:
    args = {}
    for vname, default_value in IMPORTANT_ENVS.items():
        if vname in dockerfile_content:
            value = os.environ.get(vname, default_value)
            args[vname] = value

    # Put it always
    if ENV_REGISTRY not in args:
        args[ENV_REGISTRY] = os.environ.get(ENV_REGISTRY, IMPORTANT_ENVS[ENV_REGISTRY])

    # args["AIDO_REGISTRY"] = args[ENV_REGISTRY]  # OLD support
    return args


def get_important_env_build_args(dockerfile_content: str) -> List[str]:
    ds = get_important_env_build_args_dict(dockerfile_content)
    args = []
    for k, v in ds.items():
        args.extend(["--build-arg", f"{k}={v}"])
    return args
