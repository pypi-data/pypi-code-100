from typing import *
from .exception import *


class SymbolTable:

    def __init__(self):
        self.symbols = dict()
    
    def insert(self, identifier, node):
        symbol = Symbol(identifier, node)
        self.symbols[identifier] = symbol

    def lookup(self, identifier):
        if (identifier not in self.symbols):
            raise RuntimeException(f'{identifier} not defined')
        return self.symbols[identifier]

    def to_dict(self):
        return self.symbols


class Function(SymbolTable):

    def __init__(self, arguments, body):
        super().__init__()
        self.arguments = arguments
        self.body = body

    def get_arguments(self):
        return self.arguments

    def get_body(self):
        return self.body


class Symbol:

    def __init__(self, identifier, node):
        self.identifier = identifier
        self.node = node

    def get_identifier(self):
        return self.identifier

    def get_node(self):
        return self.node

    def is_function(self):
        return isinstance(self.node, Function)
