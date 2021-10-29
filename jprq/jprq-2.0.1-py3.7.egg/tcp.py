import asyncio
import socket


async def pump_read_to_write(read_conn, write_conn):
    size = 1024
    loop = asyncio.get_event_loop()
    buffer = await loop.sock_recv(read_conn, size)

    while buffer:
        await loop.sock_sendall(write_conn, buffer)
        buffer = await loop.sock_recv(read_conn, size)

    read_conn.close()
    write_conn.close()


class Client:
    def __init__(self, remote_server_host, remote_server_port, local_server_host, local_server_port):
        self.remote_server_host = remote_server_host
        self.remote_server_port = remote_server_port
        self.local_server_host = local_server_host
        self.local_server_port = local_server_port

    async def process(self, message, websocket):
        remote_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_client.connect((self.remote_server_host, self.remote_server_port))

        local_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        local_client.connect((self.local_server_host, self.local_server_port))

        port = message["public_client_port"]
        remote_client.send(bytearray([port >> 8 & 0xFF, port & 0xFF]))  # 16 bits

        remote_client.setblocking(False)
        local_client.setblocking(False)

        asyncio.ensure_future(pump_read_to_write(remote_client, local_client))
        asyncio.ensure_future(pump_read_to_write(local_client, remote_client))
