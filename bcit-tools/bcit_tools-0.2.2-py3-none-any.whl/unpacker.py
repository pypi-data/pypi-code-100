import logging
import shutil
from pathlib import Path

from .helpers import (
    d2l_zip_to_student_files,
    match_student_path,
    move_student_files,
    unzip,
)

logging.basicConfig(format="%(levelname)s\t%(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


def organize_student_folder(student_folder: Path):
    # Look for ZIP files
    zip_files = list(student_folder.glob("*.zip"))
    for zipf in zip_files:
        unzip(zipf)
        zipf.unlink()

    if len(zip_files) > 1:
        logger.warning(f"More than 1 zip file in folder {student_folder.name}.")
        return

    # If there is only one folder, move all its files to the student folder
    folders = [p for p in student_folder.iterdir() if p.is_dir()]
    if len(folders) == 1:
        for file in folders[0].iterdir():
            shutil.move(file, student_folder)
        try:
            folders[0].unlink()
        except PermissionError as e:
            logger.warning("Exception occurred: %s", e)


def d2l_unpack(folder: str):
    path = Path(folder)
    # Unpack D2L archive
    archive_found = d2l_zip_to_student_files(path)
    if archive_found is False:
        return False

    # Organize files into folders
    for student_file in path.iterdir():
        matches = match_student_path(student_file)
        if not matches:
            continue
        move_student_files(path, matches["student_id"], matches["student_name"])

    # Extract / organize files inside student folders
    for student_folder in path.iterdir():
        if not student_folder.is_dir():
            continue

        organize_student_folder(student_folder)
