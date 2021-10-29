from hurry.filesize import size, alternative

def filesize(bytes_int: int):
    return size(bytes_int, system=alternative)