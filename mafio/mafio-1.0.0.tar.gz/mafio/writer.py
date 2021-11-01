"""Module for writing MAF files. It contains a single write function that writes
the data into a MAF file with optional compression.
"""
import gzip


def write(path, data, append=False):
    """Write or append data into a MAF file with optional compression. It compresses the
    data into a gzip file when passed a path containing .gz

    Args:
        path (string): Path to the file. Creates the file if it doesn't exist.
        When passed a path that ends with .gz, it compresses the data.
        data (ndarray): Data to write into the file.
        append (bool, optional): Append the data in the existing file. Defaults to False.
    """
    mode = "wb"
    parser = open
    if append:
        mode = "ab"
    if path.endswith(".gz"):
        parser = gzip.open

    with parser(path, mode) as file:
        raw_data = ""
        for row in data:
            raw_data = raw_data + \
                "".join([str(val) + "\t" for val in row]).rstrip("\t") + "\n"
        file.write(raw_data.encode())