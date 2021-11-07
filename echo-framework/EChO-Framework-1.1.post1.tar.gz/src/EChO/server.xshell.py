import paramiko

def do(host, p,  user, psw, cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(hostname=host, port=p, username=user, password=psw)
    stdin, stdout, stderr = ssh.exec_command(cmd)

    result = stdout.read()

    if not result:
        result = stderr.read()
    ssh.close()

    return result.decode()