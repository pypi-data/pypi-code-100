# a script for simpliefiying the communication between the server and the client
# server:
#   setup() -> inits the server
#   new_connection() -> adds a new connection to the server with the given id
#   get() -> tries to get the a message from the client with the specified id
#   post() -> sends a message to the clients with the given id(s)
#
# client:
#    setup() -> inits the client
#    connect() -> conntects to the server with the specified ip and port
#    get() -> tries to get a message from the server
#    post() -> sends a message to the server

from socket import *
from pickle import loads, dumps
from typing import Any


class NetworkingException(Exception):
    pass


class Server:
    def __init__(self, debug: bool = True) -> None:
        self.ip: str = None; self.port: int = None
        self.connections: dict[str, socket] = {}

        self.debug: bool = debug

    def setup(self, ip: str = gethostbyname(gethostname()), port: int = 1234, listen_to: int = 5) -> None:
        self.ip: str = ip; self.port: int = port
        # create server
        self.server: socket = socket(AF_INET, SOCK_STREAM)
        self.server.bind((self.ip, self.port))
        self.server.listen(listen_to)
        self.print(f"Server open with IP {self.ip} on Port '{self.port}'\n")

    def new_connection(self, id: str) -> None:
        # validate id
        if id in self.connections:
            raise NetworkingException("Id already used") # there is already a connection with this id
        else:
            self.print(f"Waiting for new connection with id {id}")
            self.connections[id], (remoteinf) = self.server.accept() # accepting the next connection
            self.print(f"{remoteinf[0]}:{remoteinf[1]} connected with id '{id}'\n")

    def get(self, id: str) -> Any: # get a message
        try:
            return loads(self.connections[id].recv(1024))
        except ConnectionResetError: # connection lost, client is not available anymore
            raise NetworkingException("Connection lost")

    def post(self, ids: list[str], content: str) -> None: # post a message to the specified clients
        for id in ids:
            if id in self.connections: # loop through all given ids
                try:
                    self.connections[id].send(dumps(content)) # send content
                except ConnectionResetError: # connection lost, client is not available anymore
                    raise NetworkingException("Connection lost")

    def print(self, string):
        if self.debug:
            print(string)


class Client:
    def __init__(self, debug: bool = True) -> None:
        self.ip, self.port = None, None

        self.debug = debug

    def setup(self, ip: str = gethostbyname(gethostname()), port: int = 1234):
        self.ip, self.port = ip, port
        # create client and connect to server
        self.client = socket(AF_INET, SOCK_STREAM)
        self.connect()

    def connect(self) -> None:
        try:
            self.client.connect((self.ip, self.port)) # connect to the server
        except ConnectionRefusedError: # server is not available
            raise NetworkingException("The server refused a connection")
        self.print(f"Connected to {self.ip} on port {self.port}\n")

    def get(self) -> Any:
        try:
            return loads(self.client.recv(1024)) # get a message from the server
        except ConnectionResetError: # connection lost, server is not available anymore
            raise NetworkingException("Connection lost")

    def post(self, content: str) -> None:
        try:
            self.client.send(dumps(content)) # send a message to the server
        except ConnectionResetError: # connection lost, server is not available anymore
            raise NetworkingException("Connection lost")

    def print(self, string):
        if self.debug:
            print(string)
