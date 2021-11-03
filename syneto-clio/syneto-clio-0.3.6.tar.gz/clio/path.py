import pipes

from clio.shell import Shell


class Path:
    @staticmethod
    def exists_remote(host, password, path) -> bool:
        command = f"sshpass -p {password} ssh -o 'StrictHostKeyChecking=no' {host} test -e {pipes.quote(path)}"
        result = Shell.run(command=command, without_stdout=True)
        if result.returncode == 0:
            return True
        return False
