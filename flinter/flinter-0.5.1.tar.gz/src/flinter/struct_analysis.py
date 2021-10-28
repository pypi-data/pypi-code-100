"""
Strucure analysis
=============================

The rules are quite limited right now (only 6).

"""

from flinter.extension import FlintExtension, node_printer
import lizard


__all__ = ["scan_fortran_file"]


def my_token(match):
    return match

def scan_fortran_file(path, content, rules):
    """
    :params content: list of lines in FORTRAN
    """
    ext = FlintExtension(path, rules["syntax"], rules["struct-rules"], rules["regexp-rules"])
    exts = lizard.get_extensions([ext, ext.down_stream])
    context = lizard.FileInfoBuilder(path)
    reader = lizard.get_reader_for(path)
    if reader is None:
        raise ValueError
    reader = reader(context)
    tokens = reader.generate_tokens(content, "", my_token)
    for processor in exts:
        tokens = processor(tokens, reader)
    try:
        for _ in reader(tokens, reader):
            pass
    except Exception as e:
        print(path, ":", e)
    #node_printer(ext.struct[0])
    return ext.struct[0]