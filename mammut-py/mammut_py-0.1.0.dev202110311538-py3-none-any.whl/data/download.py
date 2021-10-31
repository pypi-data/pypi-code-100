# coding=utf-8
from __future__ import ( division, absolute_import, print_function, unicode_literals )

import sys, os

if sys.version_info >= (3,):
    import urllib.request as urlrequest
    import urllib.parse as urlparse
    import bz2
    import gzip
else:
    import urllib2 as urlrequest
    import urlparse
    import bz2
    import gzip


def file(url, directory, file=None):
    u = urlrequest.urlopen(url)

    scheme, netloc, path, query, fragment = urlparse.urlsplit(url)

    if not file:
        file = os.path.basename(path)

    filename = os.path.join(directory, file)
    if os.path.isfile(filename):
        return filename

    with open(filename, 'wb') as f:
        meta = u.info()
        meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
        meta_length = meta_func("Content-Length")
        file_size = None
        if meta_length:
            file_size = int(meta_length[0])
        print("Downloading: {0} Bytes: {1}".format(url, file_size))

        file_size_dl = 0
        block_sz = 8192
        while file_size_dl < file_size:
            reminder = file_size - file_size_dl
            if reminder < block_sz:
                block_sz = reminder
            buffer = u.read(block_sz)

            file_size_dl += len(buffer)
            f.write(buffer)

            status = "{0:16}".format(file_size_dl)
            if file_size:
                status += "   [{0:6.2f}%]".format(file_size_dl * 100 / file_size)
            status += chr(13)
            print(status, end="")
        print()

    return filename

def decompress_bz2(compressed_file, decompressed_file=None):
    if not decompressed_file:
        decompressed_file = os.path.splitext(compressed_file)[0]
    if os.path.isfile(decompressed_file):
        return decompressed_file
    with open(decompressed_file, 'wb') as new_file, bz2.BZ2File(compressed_file, 'rb') as file:
        for data in iter(lambda: file.read(100 * 1024), b''):
            new_file.write(data)

    return decompressed_file

def decompress_gz(compressed_file, decompressed_file=None):
    if not decompressed_file:
        decompressed_file = os.path.splitext(compressed_file)[0]
    if os.path.isfile(decompressed_file):
        return decompressed_file
    with open(decompressed_file, 'wb') as new_file, gzip.open(compressed_file, 'rb') as file:
        for data in iter(lambda: file.read(100 * 1024), b''):
            new_file.write(data)

    return decompressed_file