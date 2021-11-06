import sys
from abc import ABC, abstractmethod
from typing import TextIO


class TextFilter(ABC):
    def __init__(self, reader: TextIO = None, writer: TextIO = None):
        self.reader = reader or sys.stdin
        self.writer = writer or sys.stdout

    @abstractmethod
    def main(self, line: str) -> str:
        raise NotImplementedError

    def run(self):
        for line in self.reader:
            filtered = str(self.main(line.strip()))
            self.writer.write(filtered + '\n')
