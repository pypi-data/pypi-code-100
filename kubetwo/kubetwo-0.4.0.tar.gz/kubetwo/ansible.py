from pathlib import Path
import shutil
from typing import Dict, List

import ruamel.yaml
from termcolor import cprint

from kubetwo.config import ArtifactSettings, Settings
from kubetwo.common import Common
from kubetwo.exception import *


class Ansible:

    def __init__(self,
        cluster_name: str,
        user_name: str
    ):
        self.cluster_name = cluster_name
        self.user_name = user_name
        self.ssh_private_key_path = Common.get_ssh_private_key_path()
        self.artifact = ArtifactSettings(cluster_name)

    def run_kubespray_create(self):
        command = f"""
            ansible-playbook
            --inventory {str(self.artifact.RENDERED_INVENTORY_PATH)}
            --user {self.user_name}
            --private-key {str(self.ssh_private_key_path)}
            --become
            --become-user=root
            cluster.yml
        """
        command = self._format_command(command)
        try:
            cprint("Creating Kubernetes cluster...")
            Common.run_command(command, cwd=str(self.artifact.KUBESPRAY_DIR_PATH))
            cprint("Finished to create Kubernetes cluster.\n")
        except ProcessException as err:
            raise AnsibleKubesprayException(str(err))

    def run_kubespray_scale_in(self, remove_nodes: List[str]):
        remove_nodes = ",".join(remove_nodes)
        command = f"""
            ansible-playbook
            --inventory {str(self.artifact.RENDERED_INVENTORY_PATH)}
            --user {self.user_name}
            --private-key {str(self.ssh_private_key_path)}
            --become
            --become-user=root
            --extra-vars "node={remove_nodes}" 
            --extra-vars "delete_nodes_confirmation=yes"
            remove-node.yml
        """
        command = self._format_command(command)
        try:
            cprint("Scaling in Kubernetes cluster...")
            Common.run_command(command, cwd=str(self.artifact.KUBESPRAY_DIR_PATH))
            cprint("Finished to scale in Kubernetes cluster.\n")
        except ProcessException as err:
            raise AnsibleKubesprayException(str(err))

    def run_kubespray_scale_out(self):
        command = f"""
            ansible-playbook
            --inventory {str(self.artifact.RENDERED_INVENTORY_PATH)}
            --user {self.user_name}
            --private-key {str(self.ssh_private_key_path)}
            --become
            --become-user=root
            scale.yml
        """
        command = self._format_command(command)
        try:
            cprint("Scaling out Kubernetes cluster...")
            Common.run_command(command, cwd=str(self.artifact.KUBESPRAY_DIR_PATH))
            cprint("Finished to scale out Kubernetes cluster.\n")
        except ProcessException as err:
            raise AnsibleKubesprayException(str(err))

    def run_setup_kubeconfig(self):
        playbook_dir_path = Settings.ANSIBLE_TEMPLATE_DIR_PATH
        command = f"""
            ansible-playbook
            --inventory {str(self.artifact.RENDERED_INVENTORY_PATH)}
            --user {self.user_name}
            --private-key {str(self.ssh_private_key_path)}
            setup_kubeconfig.yml
        """
        command = self._format_command(command)
        try:
            cprint("Setting up Kubernetes cluster...")
            Common.run_command(command, cwd=str(playbook_dir_path))
            cprint("Finished to set up Kubernetes cluster.\n")
        except ProcessException as err:
            raise AnsibleSetupException(str(err))

    def run_fetch_kubeconfig(
        self,
        artifact_dir_path: Path,
        admin_conf_path: Path,
        rendered_tfstate_path: Path
    ):
        playbook_dir_path = Settings.ANSIBLE_TEMPLATE_DIR_PATH
        command = f"""
            ansible-playbook
            --inventory {str(self.artifact.RENDERED_INVENTORY_PATH)}
            --user {self.user_name}
            --private-key {str(self.ssh_private_key_path)}
            --extra-vars dest_path={str(artifact_dir_path)}
            fetch_kubeconfig.yml
        """
        command = self._format_command(command)
        try:
            cprint("Fetching admin.conf from control plane...")
            Common.run_command(command, cwd=str(playbook_dir_path))
            control_planes = Common.get_control_planes(rendered_tfstate_path)
            shutil.copy(artifact_dir_path / f"{control_planes[0]['name']}/admin.conf", admin_conf_path)
            for control_plane in control_planes:
                shutil.rmtree(str(artifact_dir_path / f"{control_plane['name']}"))
            cprint("Finished to fetch admin.conf from control plane.\n")
        except ProcessException as err:
            raise AnsibleFetchAdminConfException(str(err))

    def render_inventory(self):
        cprint("Rendering inventory file for Ansible...")
        yaml = ruamel.yaml.YAML()
        control_plane_list = Common.get_control_planes(self.artifact.RENDERED_TFSTATE_PATH)
        worker_node_list = Common.get_worker_nodes(self.artifact.RENDERED_TFSTATE_PATH)

        if len(control_plane_list) % 2 == 0:
            etcd_count = len(control_plane_list) - 1
        else:
            etcd_count = len(control_plane_list)

        with open(Settings.INVENTORY_PATH, "r") as stream:
            inventory = yaml.load(stream)

        for node in control_plane_list + worker_node_list:
            inventory["all"]["hosts"][node["name"]] = {
                "ansible_ssh_host": node["public_ip"],
                "ip": node["private_ip"],
                "access_ip": node["private_ip"]
            }

        for control_plane in control_plane_list:
            inventory["all"]["children"]["kube_control_plane"]["hosts"][control_plane["name"]] = None

        for worker_node in worker_node_list:
            inventory["all"]["children"]["kube_node"]["hosts"][worker_node["name"]] = None

        for control_plane in control_plane_list[:etcd_count]:
            inventory["all"]["children"]["etcd"]["hosts"][control_plane["name"]] = None

        all_vars = {
            "loadbalancer_apiserver": {"port": 6443},
            "loadbalancer_apiserver_localhost": False,
            "loadbalancer_apiserver_port": 6443,
            "apiserver_loadbalancer_domain_name": Common.get_control_plane_lb_dns(self.artifact.RENDERED_TFSTATE_PATH),
            "ansible_ssh_common_args": "-o ControlMaster=auto -o ControlPersist=60s -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"
        }
        k8s_cluster_group_vars = {
            "ingress_nginx_enabled": True,
            "ingress_nginx_host_network": True,
            "helm_enabled": True
        }
        inventory["all"]["vars"] = all_vars
        inventory["all"]["children"]["k8s_cluster"]["vars"] = k8s_cluster_group_vars

        with open(self.artifact.RENDERED_INVENTORY_PATH, "w") as stream:
            yaml.dump(inventory, stream=stream)

        cprint(f"Finished to render inventory file ({self.artifact.RENDERED_INVENTORY_PATH}).\n")

    def copy_group_vars(self):
        cprint("Copying group vars for Ansible...")
        src = str(self.artifact.KUBESPRAY_GROUP_VARS_DIR_PATH)
        dest = str(self.artifact.RENDERED_KUBESPRAY_GROUP_VARS_DIR_PATH)
        shutil.copytree(src, dest)
        cprint("Finished to copy group vars.\n", "cyan")

    def _format_command(self, command: str) -> str:
        command = command.replace("\n", " ")
        command = " ".join(command.split())
        return command
