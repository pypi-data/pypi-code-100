import json
import os
from pathlib import Path
import subprocess
from typing import Any, Dict, List, Tuple

from jinja2 import Template
from pydantic import BaseModel
from termcolor import cprint

from kubetwo.config import Settings
from kubetwo.exception import *


class Common:

    @classmethod
    def run_command(cls, command: str, cwd: str=None, stdout: bool=True):
        stdout = None if stdout else subprocess.DEVNULL
        try:
            process = subprocess.run(
                command,
                shell=True,
                stdout=stdout,
                stderr=subprocess.PIPE,
                cwd=cwd
            )
            process.check_returncode()
        except subprocess.CalledProcessError as err:
            raise ProcessException(process.stderr.decode("utf8"))
        except KeyboardInterrupt as err:
            raise CheckDeniedException("[ERROR] Suspended to execute command.\n")
        
    @classmethod
    def get_control_planes(cls, rendered_tfstate_path: Path) -> List[Dict[str, str]]:
        private_ips = cls._get_value_from_tfstate("control_plane_private_ips", rendered_tfstate_path)
        public_ips = cls._get_value_from_tfstate("control_plane_public_ips", rendered_tfstate_path)

        control_planes = []
        for i, (private_ip, public_ip) in enumerate(zip(private_ips, public_ips)):
            name = f"control-plane{i}"
            control_planes.append({"name": name, "private_ip": private_ip, "public_ip": public_ip})

        return control_planes

    @classmethod
    def get_worker_nodes(cls, rendered_tfstate_path: Path) -> List[Dict[str, str]]:
        private_ips = cls._get_value_from_tfstate("worker_node_private_ips", rendered_tfstate_path)
        public_ips = cls._get_value_from_tfstate("worker_node_public_ips", rendered_tfstate_path)

        worker_nodes = []
        for i, (private_ip, public_ip) in enumerate(zip(private_ips, public_ips)):
            name = f"worker-node{i}"
            worker_nodes.append({"name": name, "private_ip": private_ip, "public_ip": public_ip})

        return worker_nodes
 
    @classmethod
    def get_control_plane_lb_dns(cls, rendered_tfstate_path: Path) -> str:
        return cls._get_value_from_tfstate("control_plane_lb_dns", rendered_tfstate_path)

    @classmethod
    def get_ami(cls, rendered_tfstate_path: Path) -> str:
        return cls._get_value_from_tfstate("ami", rendered_tfstate_path)

    @classmethod
    def get_instance_type(cls, rendered_tfstate_path: Path) -> str:
        return cls._get_value_from_tfstate("instance_type", rendered_tfstate_path)

    @classmethod
    def get_ports(cls, rendered_tfstate_path: Path) -> List[int]:
        return cls._get_value_from_tfstate("ports", rendered_tfstate_path)

    @classmethod
    def get_default_user_name(cls, rendered_tfstate_path: Path) -> str:
        with open(rendered_tfstate_path, "r") as f:
            tfstate_data = json.load(f)

        ami_name = tfstate_data["outputs"]["ami_name"]["value"]
        ami_description = tfstate_data["outputs"]["ami_description"]["value"]
        ami_location = tfstate_data["outputs"]["ami_location"]["value"]

        with open(Settings.DISTRO_INFO_FILE_PATH, "r") as file:
            distro_list = json.load(file)

        default_user_name = "ec2-user"
        for distro in distro_list:
            if  (
                distro["ami_name_keyword"] in ami_name or
                distro["ami_description_keyword"] in ami_description or
                distro["ami_location_keyword"] in ami_location
                ):
                distro_name = distro["distro_name"]
                cprint(f"{distro_name} is detected.")
                default_user_name = distro["user_name"]
                break
                
        cprint(f"User \"{default_user_name}\" will be used for EC2 default user.\n")
        return default_user_name

    @classmethod
    def show_node_info(cls, rendered_tfstate_path: Path):
        control_plane_list = cls.get_control_planes(rendered_tfstate_path)
        worker_node_list = cls.get_worker_nodes(rendered_tfstate_path)
        user_name = cls.get_default_user_name(rendered_tfstate_path)
        params = {
            "control_plane_list": control_plane_list,
            "worker_node_list": worker_node_list,
            "user_name": user_name,
            "ssh_private_key": str(Common.get_ssh_private_key_path())
        }
        with open(Settings.NODE_INFO_FILE_PATH, "r") as file:
            template = Template(file.read())

        node_info = template.render(params)
        cprint(node_info, "cyan")

    @classmethod
    def get_ssh_public_key_path(cls):
        return Path(os.environ.get("SSH_PUBLIC_KEY_PATH")).expanduser()

    @classmethod
    def get_ssh_private_key_path(cls):
        return Path(os.environ.get("SSH_PRIVATE_KEY_PATH")).expanduser()

    @classmethod
    def _get_value_from_tfstate(cls, name: str, rendered_tfstate_path: Path) -> Any:
        if not os.path.exists(str(rendered_tfstate_path)):
            raise TerraformStateNotFound(f"""
                [ERROR] terraform.tfstate doesn't exist at {str(rendered_tfstate_path)}
                It's necessary to execute kubetwo init command first""")

        with open(rendered_tfstate_path, "r") as f:
            tfstate_data = json.load(f)
        return tfstate_data["outputs"][name]["value"]
