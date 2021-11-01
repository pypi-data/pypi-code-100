import os
import re
import shutil
import logging

logging.basicConfig(
    level = logging.INFO,
    format = '%(message)s',
)


def delete_files(parent_path, fmt, delete_type=0):
    # Children list of parent directory
    children = os.listdir(parent_path)
    # Return if children list is empty
    if not children:
        return
    # Traverse all children
    for child in children:
        # Full path of current child
        child_path = os.path.join(parent_path, child)
        # Files deletion required
        if delete_type in (0, 1):
            # Current child is a file
            if os.path.isfile(child_path):
                # Delete the file if eligible
                if re.search(fmt, child):
                    os.remove(child_path)
                    logging.info("Deleting file: " + child_path)
            # Continue depth first search if current child is a directory
            else:
                # Continue depth first search
                delete_files(child_path, fmt, delete_type)
        # Directories deletion required
        if delete_type in (0, 2):
            # Ignore if current child is a file
            if not os.path.isdir(child_path):
                continue
            # Delete if current child is a directory and eligible
            elif re.search(fmt, child):
                shutil.rmtree(child_path) # Delete a non-empty directory
                print("Deleting directoty: " + child_path)
            # Continue depth first search if current child is a directory but not eligible
            else:
                delete_files(child_path, fmt, delete_type)