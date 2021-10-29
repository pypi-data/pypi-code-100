try:
    import pathlib
except ImportError:
    pass


_NUM_SIGNATURE_BYTES = 262


def get_signature_bytes(path):
    """
    从文件中读取前262个字节。
    """
    with open(path, "rb") as fp:
        return bytearray(fp.read(_NUM_SIGNATURE_BYTES))


def signature(array):
    """
    截取字节数组的前262字节。
    """
    length = len(array)
    index = _NUM_SIGNATURE_BYTES if length > _NUM_SIGNATURE_BYTES else length

    return array[:index]


def get_bytes(obj):
    """
    判断输入类型，并读取前262个字节，返回一个字节数组
    """
    kind = type(obj)

    if kind is bytearray:
        return signature(obj)

    if kind is str:
        return get_signature_bytes(obj)

    if kind is bytes:
        return signature(obj)

    if kind is memoryview:
        return bytearray((signature(obj).tolist()))

    if isinstance(obj, pathlib.PurePath):
        return get_signature_bytes(obj)

    raise TypeError("Unsupported type as file input: %s" % kind)
