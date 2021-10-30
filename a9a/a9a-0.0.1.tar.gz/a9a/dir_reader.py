import pathlib

DIRECTORY = 0
EXECUTABLE = 1
FILE = 2
LINK = 3


def read_node(path):
    path = pathlib.Path(path)
    if path.is_symlink():
        return read_link(path)
    if path.is_dir():
        return read_directory(path)
    if not path.is_file():
        assert False
    mode = path.stat().st_mode
    mode, x0 = divmod(mode, 8)
    mode, x1 = divmod(mode, 8)
    mode, x2 = divmod(mode, 8)
    if x0 & x1 & x2 & 1:
        return read_executable(path)
    return read_file(path)


def read_link(path):
    path = pathlib.Path(path)
    return (LINK, bytes(path.readlink()))


def read_directory(path):
    path = pathlib.Path(path)
    nodes = {p.name.encode(): read_node(p) for p in path.iterdir()}
    return (DIRECTORY, nodes)


def read_executable(path):
    path = pathlib.Path(path)
    with path.open("rb") as f:
        content = f.read()
    return (EXECUTABLE, content)


def read_file(path):
    path = pathlib.Path(path)
    with path.open("rb") as f:
        content = f.read()
    return (FILE, content)
