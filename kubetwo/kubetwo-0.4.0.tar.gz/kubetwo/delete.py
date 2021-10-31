import os
import shutil

from termcolor import cprint

from kubetwo.model import DeleteInput
from kubetwo.config import ArtifactSettings
from kubetwo.terraform import Terraform
from kubetwo.exception import *


class Delete:

    def __init__(self, input: DeleteInput):
        self.input = input
        self.artifact = ArtifactSettings(self.input.cluster_name)
        self.terraform = Terraform(self.input.cluster_name)

    def run(self):
        self.terraform.show_plan(destroy_mode=True)
        if not self.input.approve:
            self.check_tf_plan()
        self.terraform.destroy()
        if not self.input.approve:
            self.check_delete_dir()
        self.delete_dir()

    def check_tf_plan(self):
        cprint(f"Newly created AWS resources will be removed.", "yellow")
        cprint("Do you proceed?\n", "yellow")
        try:
            choice = input("Enter a value [y/N]: ")
            if choice.lower() in ['y', 'yes']:
                return
        except KeyboardInterrupt:
            print()

        raise CheckDeniedException("[ERROR] Suspended to remove AWS resources.")

    def check_delete_dir(self):
        cprint(f"{self.artifact.ARTIFACT_DIR_PATH} will be deleted.", "yellow")
        cprint("Do you proceed?\n", "yellow")
        try:
            choice = input("Enter a value [y/N]: ")
            if choice.lower() in ['y', 'yes']:
                return
        except KeyboardInterrupt:
            print()
        
        raise CheckDeniedException("[ERROR] Suspended to delete workspace.")

    def delete_dir(self):
        if os.path.isdir(str(self.artifact.ARTIFACT_DIR_PATH)):
            shutil.rmtree(str(self.artifact.ARTIFACT_DIR_PATH))
        cprint("Finished to clean workspace.\n", "cyan")
