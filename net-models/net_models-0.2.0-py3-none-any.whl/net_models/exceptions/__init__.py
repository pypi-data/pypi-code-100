class NetModelException(Exception):
    pass

class InterfaceAlreadyExists(NetModelException):
    pass

class HostNotFound(NetModelException):
    pass

class GroupNotFound(NetModelException):
    pass

class VlanNotFound(NetModelException):
    pass