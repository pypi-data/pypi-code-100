from pathlib import Path


def valid_dir_name(name: str) -> str:
    name = name.lower()
    if not name.isidentifier():
        raise ValueError(
            "Please enter valid name containing only characters and underscores."
        )
    return name


def validate_path_does_not_exist(p: Path) -> bool:
    if p.exists():
        raise FileExistsError(f"Directory with path '{p}' already exists.")
    return True
