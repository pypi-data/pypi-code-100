import os
from pathlib import Path
from typing import Any, List

from jinja2 import Template

from kubetwo.config import ArtifactSettings, Settings


class Validator:
    """Collection of validation method for pydantic BaseModel"""

    @classmethod
    def str_to_path(cls, str_path: str) -> Path:
        try:
            return Path(str_path).expanduser()
        except:
            raise ValueError("is invalid format.")

    @classmethod
    def file_exists(cls, file_path: Path) -> Path:
        if not os.path.isfile(file_path):
            raise ValueError("file doesn't exist")
        return file_path

    @classmethod
    def artifact_dir_exists(cls, _, values: Any) -> Any:
        if not values.get("cluster_name"):
            return values

        artifact_dir_path = ArtifactSettings(values["cluster_name"]).ARTIFACT_DIR_PATH
        if not os.path.isdir(str(artifact_dir_path)):
            raise ValueError(f"\"{artifact_dir_path.name}\" doesn't exist in current place.")
        return values

    @classmethod
    def tfstate_exists(cls, _, values: Any) -> Any:
        if not values.get("cluster_name"):
            return values

        tfstate_path = ArtifactSettings(values["cluster_name"]).RENDERED_TFSTATE_PATH
        if not os.path.isfile(str(tfstate_path)):
            relative_tfstate_path = tfstate_path.relative_to(Path.cwd())
            raise ValueError(f"\"{relative_tfstate_path}\" doesn't exist in current place.")
        return values

    @classmethod
    def is_credentials_registered(cls, _, values: Any) -> Any:
        error_message = ""
        not_defined_environment_valiables = []
        for environment_variable_name in ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_DEFAULT_REGION"]:
            if not os.environ.get(environment_variable_name):
                not_defined_environment_valiables.append(environment_variable_name)

        if not_defined_environment_valiables:
            error_message = ", ".join(not_defined_environment_valiables)
            if len(not_defined_environment_valiables) == 1:
                error_message += " is not defined as an environment variable"
            else:
                error_message += " are not defined as an environment variables"

        if error_message:
            raise ValueError(error_message)
            
        return values

    @classmethod
    def is_ssh_keys_registered(cls, _, values: Any) -> Any:
        error_message = ""
        not_defined_environment_valiables = []
        for environment_variable_name in ["SSH_PUBLIC_KEY_PATH", "SSH_PRIVATE_KEY_PATH"]:
            if not os.environ.get(environment_variable_name):
                not_defined_environment_valiables.append(environment_variable_name)

        if not_defined_environment_valiables:
            error_message = ", ".join(not_defined_environment_valiables)
            if len(not_defined_environment_valiables) == 1:
                error_message += " is not defined as an environment variable"
            else:
                error_message += " are not defined as an environment variables"

        if error_message:
            raise ValueError(error_message)
            
        return values

    @classmethod
    def is_ssh_keys_exist(cls, _, values: Any) -> Any:
        error_message = ""
        not_exist_ssh_keys = []

        for environment_variable_name in ["SSH_PUBLIC_KEY_PATH", "SSH_PRIVATE_KEY_PATH"]:
            key_str_path = os.environ.get(environment_variable_name)                
            try:
                Path(key_str_path).expanduser()
            except:
                not_exist_ssh_keys.append(environment_variable_name)
                continue
            
            if not Path(key_str_path).expanduser().exists():
                not_exist_ssh_keys.append(environment_variable_name)

        if not_exist_ssh_keys:
            error_message = ", ".join(not_exist_ssh_keys)
            if len(not_exist_ssh_keys) == 1:
                error_message += " doesn't exist"
            else:
                error_message += " don't exist"
        
        if error_message:
            raise ValueError(error_message)
        
        return values


class ValidationFormatter:

    @classmethod
    def format(cls, results: List) -> str:
        with open(Settings.VALIDATION_RESULT_FILE_PATH, "r") as file:
            template = Template(file.read())
        
        results_for_template = {}
        for result in results:
            locs = [str(elem) for elem in result["loc"]]
            loc = " ".join(locs)
            if loc == "__root__":
                loc = "others"
            if results_for_template.get(loc):
                results_for_template[loc].append(result["msg"])
            else:
                results_for_template[loc] = [result["msg"]]
            
        params = {"results": results_for_template}
        
        formatted_result = template.render(params)
        return formatted_result
