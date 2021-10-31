import os
import shutil
import tarfile

import requests
from termcolor import cprint

from kubetwo.model import CreateInput
from kubetwo.common import Common
from kubetwo.config import ArtifactSettings, Settings
from kubetwo.ansible import Ansible
from kubetwo.exception import *
from kubetwo.terraform import Terraform


class Create:

    def __init__(self, input: CreateInput):
        self.input = input
        self.artifact = ArtifactSettings(self.input.cluster_name)

    def run(self):
        if not self.input.approve:
            self.check_clean_artifact_dir()
        self.clean_artifact_dir()
        self.download_kubespray()

        terraform = Terraform(self.input.cluster_name)
        terraform.create_terraform_manifests(**self.input.dict())
        terraform.initialize()
        terraform.show_plan()
        if not self.input.approve:
            terraform.check_tf_plan()
        terraform.apply()

        ansible = Ansible(
            self.input.cluster_name,
            Common.get_default_user_name(self.artifact.RENDERED_TFSTATE_PATH)
        )
        ansible.render_inventory()
        ansible.copy_group_vars()
        ansible.run_kubespray_create()
        ansible.run_setup_kubeconfig()
        ansible.run_fetch_kubeconfig(
            artifact_dir_path = self.artifact.ARTIFACT_DIR_PATH,
            admin_conf_path = self.artifact.ADMIN_CONF_PATH,
            rendered_tfstate_path = self.artifact.RENDERED_TFSTATE_PATH
        )

        Common.show_node_info(self.artifact.RENDERED_TFSTATE_PATH)

    def check_clean_artifact_dir(self):
        if not os.path.isdir(str(self.artifact.ARTIFACT_DIR_PATH)):
            return

        cprint(f"Directory {str(self.artifact.ARTIFACT_DIR_PATH)} already exists.", "yellow")
        cprint("Do you use this directory to setup kubetwo?\n", "yellow")
        try:
            choice = input("Enter a value [y/N]: ")
            print()
            if choice.lower() in ['y', 'yes']:
                return
        except KeyboardInterrupt:
            print()

        raise CheckDeniedException("[ERROR] Please use different cluster name.")

    def clean_artifact_dir(self):
        if not os.path.isdir(str(self.artifact.ARTIFACT_DIR_PATH)):
            os.makedirs(str(self.artifact.ARTIFACT_DIR_PATH))

        if os.path.isdir(str(self.artifact.RENDERED_ANSIBLE_DIR_PATH)):
            shutil.rmtree(str(self.artifact.RENDERED_ANSIBLE_DIR_PATH))
        os.makedirs(str(self.artifact.RENDERED_ANSIBLE_DIR_PATH))

        if not os.path.isdir(str(self.artifact.RENDERED_TERRAFORM_DIR_PATH)):
            os.makedirs(str(self.artifact.RENDERED_TERRAFORM_DIR_PATH))

        for tf_file_path in self.artifact.RENDERED_TERRAFORM_DIR_PATH.glob("**/*.tf"):
            os.remove(str(tf_file_path))

        if os.path.isfile(str(self.artifact.RENDERED_INVENTORY_PATH)):
            os.remove(str(self.artifact.RENDERED_INVENTORY_PATH))

        cprint(f"Finished to clean up {str(self.artifact.ARTIFACT_DIR_PATH)}\n")

    def download_kubespray(self):
        cprint("Downloading Kubespray...")
        if os.path.isdir(self.artifact.KUBESPRAY_DIR_PATH):
            return

        kubespray_content = requests.get(Settings.KUBESPRAY_ARCHIVE_URL).content

        with open(self.artifact.KUBESPRAY_ARCHIVE_PATH ,mode='wb') as file:
            file.write(kubespray_content)

        with tarfile.open(self.artifact.KUBESPRAY_ARCHIVE_PATH) as tar:
            tar.extractall(self.artifact.ARTIFACT_DIR_PATH)

        os.remove(str(self.artifact.KUBESPRAY_ARCHIVE_PATH))
        cprint("Finished to download Kubespray.\n")
