class ContainerException(Exception): pass
class NoContainerKey(ContainerException): pass
class NotContainerType(ContainerException, TypeError): pass
class WontOverwriteClassmethod(ContainerException): pass
class ContainerEmptyException(ContainerException): pass
class StackEmptyException(ContainerEmptyException): pass
class QueueEmptyException(ContainerEmptyException): pass