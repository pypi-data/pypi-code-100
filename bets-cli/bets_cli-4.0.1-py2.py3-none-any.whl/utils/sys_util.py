from datetime import datetime
from functools import partial
from multiprocessing import Process
from pathlib import Path
from platform import system
from shutil import copyfile, copytree
from subprocess import call
from tempfile import gettempdir

from bets.utils import log

IS_WIN = system() == "Windows"
IS_LIN = system() == "Linux"


def is_windows() -> bool:
    return system() == "Windows"


def is_linux() -> bool:
    return system() == "Linux"


def is_file(path) -> bool:
    return bool(Path(path).suffix)


def get_utc_timestamp() -> str:
    return datetime.utcnow().strftime('%Y-%m-%d_%H_%M_%S_%f')


def get_tmp_location(path: str) -> str:
    log.debug(f"getting temp location for: [{path}]")

    src_path = Path(path)
    log.debug(f"got src path: [{str(src_path)}]")

    tmp_path = str(Path(gettempdir()).joinpath("".join([src_path.stem, "_tmp_", get_utc_timestamp(), src_path.suffix])))
    log.debug(f"got temp location: [{tmp_path}]")

    return tmp_path


def delete(path: str):
    path = Path(path)

    if not path.exists():  # pragma: no cover
        raise FileNotFoundError(str(path))

    if path.is_file():
        log.debug(f"deleting file at: [{str(path)}]")
        path.unlink()
        return

    if path.is_dir():
        log.debug(f"deleting dir contents: [{str(path)}]")

        for child_path in path.iterdir():
            delete(str(child_path))

        log.debug(f"deleting dir at: [{str(path)}]")
        path.rmdir()


def copy(src_path: str, dst_path: str, exists_ok=False) -> str:
    log.debug(f"copying from [{src_path}] to [{dst_path}]")

    src_path = Path(src_path).absolute()
    if not src_path.exists():  # pragma: no cover
        raise FileNotFoundError(str(src_path))

    dst_path = Path(dst_path).absolute()
    if dst_path.exists():  # pragma: no cover
        if exists_ok:
            delete(str(dst_path))
        else:
            raise FileExistsError(str(dst_path))

    if src_path.is_file():
        log.debug(f"copying file from: [{str(src_path)}] to: [{str(dst_path)}]")
        return copyfile(str(src_path), str(dst_path))

    if src_path.is_dir():  # pragma: no cover
        log.debug(f"copying dir from: [{str(src_path)}] to: [{str(dst_path)}]")
        return copytree(str(src_path), str(dst_path))


def copy_to_tmp(src_path: str) -> str:
    dst_path = get_tmp_location(src_path)
    log.debug(f"copying [{str(src_path)}] to temp location: [{str(dst_path)}]...")
    return copy(str(src_path), str(dst_path), exists_ok=True)


def open_file(file_path: str, make_copy=True):  # pragma: no cover
    """Opens the file with the system default program handler for the type"""

    if make_copy:
        file_path = copy_to_tmp(file_path)

    open_cmd = ["cmd", "/c"] if IS_WIN else (["xdg-open"] if IS_LIN else None)
    if not open_cmd:
        raise OSError("Unsupported system!")

    process = Process(target=partial(call, open_cmd + [file_path]), daemon=True)
    process.start()
    process.join(timeout=2)


def write_text(text: str, file: str):
    path = Path(file).absolute()
    log.debug(f"writing text to: [{str(path)}] ({len(text)} chars)")
    with path.open("wb") as out:
        out.write(text.encode("utf-8"))


def view_text(text: str):
    dst_file = get_tmp_location("text_view.txt")
    write_text(text, dst_file)
    open_file(dst_file, False)
