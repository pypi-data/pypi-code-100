import socket

from firstimpression.scala import ScalaPlayer

scala = ScalaPlayer('WHITELABEL')

svars = scala.variables


class Socket:

    def __init__(self, port: int, ip: str = ''):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.buffer_size = 1024

        self.socket.bind((self.ip, self.port))

    def get_data(self):
        return self.socket.recvfrom(self.buffer_size)

    def close(self):
        self.socket.close()


def change_triggers(data: str):
    for key in svars:
        if 'Channel' in key:
            svars[key] = False

    playlist = data.split('~')[0]
    action = data.split('~')[1]

    if action == 'active':
        svars['Channel.{}'.format(playlist)] = True
