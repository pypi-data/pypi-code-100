import datetime
import logging
import operator
import os
import re
import zipfile
from collections import Counter
from pathlib import Path

logger = logging.getLogger(__name__)

STUDENT_REGEX = r"(?P<student_id>A\d{8})_(?P<student_name>[ -_\w]+)_(?P<month>\w{3}) (?P<day>\d+), (?P<year>\d+) (?P<hour>\d{1,2})(?P<minute>\d{2})( ?P<am_pm>AM|PM)?_(?P<filename>.*)$"


def filename_to_dict(path: Path):
    matches = re.search(STUDENT_REGEX, path.name)
    if not matches:
        return None

    if "am_pm" in matches.groupdict():
        raise UserWarning("AM/PM format not supported yet!")

    dt_values = ["year", "month", "day", "hour"]
    dt_string = f"{' '.join([matches[val] for val in dt_values])}:{matches['minute']}"
    dt_format = "%Y %b %d %H:%M"
    dt = datetime.datetime.strptime(dt_string, dt_format)
    dest_name = matches["filename"]
    if os.name == "nt":
        dest_name = dest_name.lower()

    return {
        "full": path.name,
        "name": matches["student_name"],
        "id": matches["student_id"],
        "date": dt,
        "filename": dest_name,
        "path": path,
    }


def match_student_path(path: Path):
    matches = re.search(STUDENT_REGEX, path.name)
    if not matches:
        logger.debug(f"File {path.name} is not a student file.")
        return False

    return matches


def unzip(zipf: Path, log=False):
    with zipfile.ZipFile(zipf, "r") as zfp:
        zfp.extractall(zipf.parent)

    if log:
        logger.info(f"Extracted D2L archive {zipf.name}.")


def d2l_zip_to_student_files(folder: Path, clean: bool = True):
    """Takes a path to a D2L zip file, and extracts it to the same folder"""
    d2l_zip_file = list(folder.glob("*.zip"))
    if not d2l_zip_file:
        logger.info(f"No D2L archive found in folder {folder.name}.")
        return False

    if len(d2l_zip_file) > 1:
        logger.warning(f"There are several ZIP files in the folder {folder.name}.")
        value = input("Type 'yes' if you want to continue: ")
        if value != "yes":
            return False

    d2l_zip_file = d2l_zip_file[0]
    unzip(d2l_zip_file)
    logger.info(f"Extracted D2L archive {d2l_zip_file.name}.")

    index_html = d2l_zip_file.parent / "index.html"
    index_html.unlink(missing_ok=True)

    if clean:
        d2l_zip_file.unlink()
        logger.info(f"Deleted zip file: {d2l_zip_file.name}.")

    return True


def remove_duplicate_student_files(student_files):
    files_info = [filename_to_dict(file) for file in student_files]
    dups = Counter([info["filename"] for info in files_info])

    for filename, count in dups.items():
        if count > 1:
            duplicate_files_info = [
                finfo for finfo in files_info if finfo["filename"] == filename
            ]
            duplicate_files_info.sort(key=operator.itemgetter("date"), reverse=True)
            to_keep = duplicate_files_info[0]
            logger.warning(f"Found duplicate: {to_keep['name']} - {filename}.")
            logger.info(f"Keeping (most recent): {to_keep['full']}")
            for to_remove in duplicate_files_info[1:]:
                logger.info(f"Removing duplicate: {to_remove['full']}.")
                to_remove["path"].unlink()


def move_student_files(path: Path, student_id: str, student_name: str):
    """Move student files to a dedicated folder based on student ID and name"""
    student_folder = path / student_name
    student_folder.mkdir(exist_ok=True)

    # Find student files
    student_files = list(path.glob(f"* {student_id}_{student_name}_*"))
    remove_duplicate_student_files(student_files)
    student_files = list(path.glob(f"* {student_id}_{student_name}_*"))

    for file in student_files:
        file_info = filename_to_dict(file)
        file.rename(student_folder / file_info["filename"])
        logger.debug(f"{file.name} => {student_folder} / {file_info['filename']}")
