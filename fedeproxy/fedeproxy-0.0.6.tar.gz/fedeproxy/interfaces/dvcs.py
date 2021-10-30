import abc


class DVCS(abc.ABC):
    @abc.abstractmethod
    def __init__(self, dir, url):
        ...

    @property
    @abc.abstractmethod
    def directory(self):
        ...

    @property
    @abc.abstractmethod
    def url(self):
        ...

    @abc.abstractmethod
    def set_url_from_directory(self):
        ...

    @property
    @abc.abstractmethod
    def hash(self):
        ...

    @abc.abstractmethod
    def log(self):
        ...

    @abc.abstractmethod
    def fetch(self, url, hash):
        ...

    @abc.abstractmethod
    def reset(self, hash):
        ...

    @abc.abstractmethod
    def clone(self, branch):
        ...

    @abc.abstractmethod
    def pull(self, branch):
        ...

    @abc.abstractmethod
    def push(self, branch):
        ...

    @abc.abstractmethod
    def commit(self, message):
        ...
