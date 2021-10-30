import pathlib
import stat

DIRECTORY = 0
EXECUTABLE = 1
FILE = 2
LINK = 3


def write_node(path, node):
    path = pathlib.Path(path)
    typ, content = node
    if typ == LINK:
        write_link(path, content)
    elif typ == DIRECTORY:
        write_directory(path, content)
    elif typ == EXECUTABLE:
        write_executable(path, content)
    elif typ == FILE:
        write_file(path, content)
    else:
        assert False


def write_link(path, content):
    path = pathlib.Path(path)
    path.symlink_to(content)


def write_directory(path, nodes):
    path = pathlib.Path(path)
    path.mkdir()
    for name, node in nodes.items():
        write_node(path / name.decode(), node)


def write_executable(path, content):
    path = pathlib.Path(path)
    with open(path, "wb") as f:
        f.write(content)
    path.chmod(path.stat().st_mode | stat.S_IEXEC)


def write_file(path, content):
    path = pathlib.Path(path)
    with open(path, "wb") as f:
        f.write(content)
