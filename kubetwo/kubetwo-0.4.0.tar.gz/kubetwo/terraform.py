import os
from pathlib import Path
from typing import List

from termcolor import cprint
from jinja2 import Template

from kubetwo.common import Common
from kubetwo.config import ArtifactSettings, Settings
from kubetwo.exception import *


class Terraform:

    def __init__(self, cluster_name: str):
        self.artifact = ArtifactSettings(cluster_name)

    def initialize(self):
        command = "terraform init"
        try:
            cprint("Initializing Terraform...")
            Common.run_command(command, cwd=str(self.artifact.RENDERED_TERRAFORM_DIR_PATH), stdout=False)
            cprint("Terraform successfully initialized.\n", "cyan")
        except ProcessException as err:
            raise TerraformInitException(str(err))

    def show_plan(self, destroy_mode=False):
        command = "terraform plan -compact-warnings"
        try:
            cprint("Preparing Terraform plan...")
            if destroy_mode:
                command = f"{command} -destroy"
            Common.run_command(command, cwd=str(self.artifact.RENDERED_TERRAFORM_DIR_PATH))
        except ProcessException as err:
            raise TerraformPlanException(str(err))

    def apply(self):
        command = "terraform apply -auto-approve"
        try:
            cprint("Changing AWS resources...")
            Common.run_command(command, cwd=str(self.artifact.RENDERED_TERRAFORM_DIR_PATH), stdout=False)
            cprint("Completed to change AWS resources.\n", "cyan")
        except ProcessException as err:
            raise TerraformApplyException(str(err))

    def destroy(self):
        command = "terraform destroy -auto-approve"
        try:
            cprint("Removing AWS resources...")
            Common.run_command(command, cwd=str(self.artifact.RENDERED_TERRAFORM_DIR_PATH), stdout=False)
            cprint("Completed to remove AWS resources.\n", "cyan")
        except ProcessException as err:
            raise TerraformDestroyException(str(err))

    def check_tf_plan(self):
        cprint("AWS resources will change.", "yellow")
        cprint("Do you proceed?\n", "yellow")
        try:
            choice = input("Enter a value [y/N]: ")
            print()
            if choice.lower() in ['y', 'yes']:
                return
        except KeyboardInterrupt:
            print()

        raise CheckDeniedException("[ERROR] Suspended to change AWS resources.")
    
    def create_terraform_manifests(
        self,
        cluster_name: str,
        control_plane: int,
        worker_node: int,
        ami: str,
        instance_type: str,
        open_ports: List[int],
        **kwargs
    ):
        cprint("Creating Terraform manifests...")
        ssh_public_key_path = Common.get_ssh_public_key_path()
        params = {
            "cluster_name": cluster_name.replace('_', '-'),
            "control_plane_count": control_plane,
            "worker_node_count": worker_node,
            "ami": ami,
            "instance_type": instance_type,
            "ssh_public_key_name": str(ssh_public_key_path.name),
            "ssh_public_key": str(ssh_public_key_path),
            "open_ports": open_ports
        }
        tf_template_paths = list(Settings.TERRAFORM_TEMPLATE_DIR_PATH.glob("**/*.tf")) + \
                            list(Settings.TERRAFORM_TEMPLATE_DIR_PATH.glob("**/*.tf.j2"))
        for path in tf_template_paths:
            with open(path, "r") as file:
                content = file.read()

            if path.suffix == ".j2":
                content = Template(content).render(params)
                
            rendered_file_name = str(path.relative_to(Settings.TERRAFORM_TEMPLATE_DIR_PATH)).replace('.j2', '')
            rendered_file_path = self.artifact.RENDERED_TERRAFORM_DIR_PATH / rendered_file_name

            if rendered_file_path.parent != self.artifact.RENDERED_TERRAFORM_DIR_PATH:
                os.makedirs(str(rendered_file_path.parent), exist_ok=True)

            with open(rendered_file_path, "w") as f:
                f.write(content)
    
        cprint("Finished to create Terraform manifests.\n", "cyan")
