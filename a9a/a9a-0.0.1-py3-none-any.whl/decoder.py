DIRECTORY = 0
EXECUTABLE = 1
FILE = 2
LINK = 3


def decode_name(bts, start=0):
    i = start
    while bts[i] != b"/"[0]:
        i += 1
    return bts[start:i], i


def decode_line(bts, start=0):
    i = start
    while bts[i] != b"\n"[0]:
        i += 1
    return bts[start:i], i


def decode_lines(bts, start=0):
    assert bts[start] == b"\n"[0]
    lines, i = [], start
    while bts[i + 1] != b"\\"[0]:
        line, i = decode_line(bts, i + 2)
        lines.append(line)
    line, i = decode_line(bts, i + 2)
    assert bts[i] == b"\n"[0]
    lines.append(line)
    return b"\n".join(lines), i + 1


def decode_nodes(bts, start=0):
    i, nodes = start, {}
    while i < len(bts) and bts[i] != b"\\"[0]:
        (name, typ, content), i = decode_node(bts, i)
        nodes[name] = (typ, content)
    return nodes, i


def decode_file(bts, start=0):
    assert bts[start] == b":"[0]
    name, i = decode_name(bts, start + 1)
    content, j = decode_lines(bts, i + 1)
    return (name, FILE, content), j


def decode_executable(bts, start=0):
    assert bts[start] == b"!"[0]
    name, i = decode_name(bts, start + 1)
    content, j = decode_lines(bts, i + 1)
    return (name, EXECUTABLE, content), j


def decode_link(bts, start=0):
    assert bts[start] == b"@"[0]
    name, i = decode_name(bts, start + 1)
    content, j = decode_lines(bts, i + 1)
    return (name, LINK, content), j


def decode_directory(bts, start=0):
    assert bts[start] == b"/"[0]
    name, i = decode_name(bts, start + 1)
    assert bts[i + 1] == b"\n"[0]
    nodes, j = decode_nodes(bts, i + 2)
    assert bts[j : j + 2] == b"\\\n"
    return (name, DIRECTORY, nodes), j + 2


def decode_node(bts, start=0):
    if bts[start] == b"/"[0]:
        return decode_directory(bts, start)
    if bts[start] == b"@"[0]:
        return decode_link(bts, start)
    if bts[start] == b"!"[0]:
        return decode_executable(bts, start)
    if bts[start] == b":"[0]:
        return decode_file(bts, start)
    assert False
