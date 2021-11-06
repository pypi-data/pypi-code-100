"""Useful functions used in multiple modules"""
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def process_input_path(input_path: str, extension: str):
    """Process input to a proper format
    In case of a folder, it returns all internal files with the desired
    extension. In case of a single file, return it as a list. If the folder is
    empty, add a proper warning.
    """
    input_path_pos = Path(input_path)
    if input_path_pos.is_dir():
        file_names = list(input_path_pos.glob(f"*.{extension}"))
        logger.info("Converting all files in a folder")
    else:
        file_names = [input_path_pos]
        logger.info("Converting a single file")

    if not file_names:
        logger.warning("Folder has no %s files. Skipping.", extension)

    return file_names
