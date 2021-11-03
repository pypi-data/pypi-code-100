import subprocess

from clio.shell import Shell


class RemoteConnectionsUtilities:
    @staticmethod
    def are_installed(pod_name) -> bool:
        check_existence_in_pod_command = f"kubectl exec -it deployment/{pod_name} -c {pod_name} -- /bin/sh -c "
        rsync_process = Shell.run(check_existence_in_pod_command + ' "rsync"')
        openssh_process = Shell.run(check_existence_in_pod_command + '"openssh"')
        sshpass_process = Shell.run(check_existence_in_pod_command + '"sshpass"')
        if rsync_process.returncode != 0:
            return False
        if openssh_process.returncode != 0:
            return False
        if sshpass_process.returncode != 0:
            return False
        return True

    @staticmethod
    def install(pod_name):
        command = f'kubectl exec -it deployment/{pod_name} -c {pod_name} -- /bin/sh -c "apk add rsync openssh sshpass"'
        subprocess.run([command], shell=True)
