DIRECTORY = 0
EXECUTABLE = 1
FILE = 2
LINK = 3


def encode_lines(content):
    lines = content.split(b"\n")
    last_line = b"\n\\" + lines[-1] + b"\n"
    return b"".join(b"\n " + l for l in lines[:-1]) + last_line


def encode_nodes(nodes):
    return b"".join(encode_node(n, t, c) for n, (t, c) in sorted(nodes.items()))


def encode_file(name, content):
    return b":" + name + b"/" + encode_lines(content)


def encode_executable(name, content):
    return b"!" + name + b"/" + encode_lines(content)


def encode_link(name, content):
    return b"@" + name + b"/" + encode_lines(content)


def encode_directory(name, content):
    return b"/" + name + b"/\n" + encode_nodes(content) + b"\\\n"


def encode_node(name, typ, content):
    if typ == DIRECTORY:
        return encode_directory(name, content)
    if typ == EXECUTABLE:
        return encode_executable(name, content)
    if typ == FILE:
        return encode_file(name, content)
    if typ == LINK:
        return encode_link(name, content)
    assert False
