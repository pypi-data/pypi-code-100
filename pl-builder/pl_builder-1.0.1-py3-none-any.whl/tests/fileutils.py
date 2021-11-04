from pathlib import Path


def are_files_equal(path1: Path, path2: Path) -> bool:
    content1 = path1.read_bytes()
    content2 = path2.read_bytes()
    return content1 == content2
