import time
import paramiko

class SshCommands:
    def __init__(self, host, port, user, key_filename):
        self.host = host
        self.port = port
        self.user = user
        self.key_filename = key_filename

    def get_connection(self):
        ssh = paramiko.SSHClient()  # Iniciamos un cliente SSH
        ssh.load_system_host_keys() #cargamos hosts conocidos
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.host, port=self.port, username=self.user, key_filename=self.key_filename) #generamos conexion
        shell = ssh.invoke_shell() #creamos canal seguro
        return shell 

    def send_string_and_wait(self, command, wait_time, should_print, shell):
        # Send the command
        shell.send(command)
        # Wait a bit, if necessary
        while not shell.recv_ready():
            time.sleep(wait_time)
        # Flush the receive buffer
        receive_buffer = shell.recv(4096)
        # Print the receive buffer, if necessary
        if should_print:
            print(str(receive_buffer,'utf-8'))

    def restart_service(self, service, password):
        shell = self.get_connection()
        #update service
        self.send_string_and_wait("sudo docker service update --env-add UPDATE=1 " + service + "\n", 2, False, shell)
        #su passwd
        self.send_string_and_wait(password + "\n", 2, True, shell)
        shell.close()
