import json
from typing import Dict, List

from pydantic import BaseModel, conint, constr, root_validator, validator
from kubetwo.common import Common

from kubetwo.config import ArtifactSettings, Settings
from kubetwo.validator import Validator


class KubetwoCreateInput(BaseModel):

    cluster_name: constr(min_length=1, max_length=64)
    ami: str = Settings.DEFAULT_AMI
    instance_type: str = Settings.DEFAULT_INSTANCE_TYPE
    control_plane: conint(ge=1) = Settings.DEFAULT_CONTROL_PLANE_NUM
    worker_node: conint(ge=1) = Settings.DEFAULT_WORKER_NODE_NUM
    open_ports: List[conint(ge=-1, le=65535)] = Settings.DEFAULT_OPEN_PORTS
    approve: bool = False

    _is_credentials_registered = root_validator(pre=True, allow_reuse=True)(Validator.is_credentials_registered)

    _is_ssh_keys_registered = root_validator(pre=True, allow_reuse=True)(Validator.is_ssh_keys_registered)

    _is_ssh_keys_exist = root_validator(pre=True, allow_reuse=True)(Validator.is_ssh_keys_exist)

    @validator("open_ports")
    def prohibit_port_0(cls, v):
        if 0 in v:
            raise ValueError("Port 0 is not allowed")
        return v


class KubetwoScaleInput(BaseModel):
    
    cluster_name: constr(min_length=1, max_length=64)
    worker_node: conint(ge=1)
    approve: bool = False

    _is_credentials_registered = root_validator(pre=True, allow_reuse=True)(Validator.is_credentials_registered)

    _is_ssh_keys_registered = root_validator(pre=True, allow_reuse=True)(Validator.is_ssh_keys_registered)

    _is_ssh_keys_exist = root_validator(pre=True, allow_reuse=True)(Validator.is_ssh_keys_exist)

    _artifact_dir_exists = root_validator(pre=True, allow_reuse=True)(Validator.artifact_dir_exists)

    _tfstate_exists = root_validator(pre=True, allow_reuse=True)(Validator.tfstate_exists)

    @validator("worker_node")
    def is_worker_node_changed(cls, v, values):
        rendered_tfstate_path = ArtifactSettings(values["cluster_name"]).RENDERED_TFSTATE_PATH
        current_worker_node = len(Common.get_worker_nodes(rendered_tfstate_path))
        if v == current_worker_node:
            raise ValueError(f"Number of worker node should be changed (current value is {v}).")
        return v

    def scale_type(self) -> str:
        rendered_tfstate_path = ArtifactSettings(self.cluster_name).RENDERED_TFSTATE_PATH
        current_worker_node = len(Common.get_worker_nodes(rendered_tfstate_path))

        return "out" if self.worker_node > current_worker_node else "in"


class KubetwoDeleteInput(BaseModel):

    cluster_name: constr(min_length=1, max_length=64)
    approve: bool = False

    _is_credentials_registered = root_validator(pre=True, allow_reuse=True)(Validator.is_credentials_registered)

    _is_ssh_keys_registered = root_validator(pre=True, allow_reuse=True)(Validator.is_ssh_keys_registered)

    _is_ssh_keys_exist = root_validator(pre=True, allow_reuse=True)(Validator.is_ssh_keys_exist)

    _artifact_dir_exists = root_validator(pre=True, allow_reuse=True)(Validator.artifact_dir_exists)

    _tfstate_exists = root_validator(pre=True, allow_reuse=True)(Validator.tfstate_exists)


class CreateInput(BaseModel):

    cluster_name: str
    ami: str
    instance_type: str
    control_plane: int
    worker_node: int
    open_ports: List[int]
    approve: bool


class ScaleInput(BaseModel):
    
    cluster_name: str
    ami: str
    instance_type: str
    control_plane: int
    worker_node: int
    open_ports: List[int]
    approve: bool


class DeleteInput(BaseModel):

    cluster_name: str
    approve: bool
