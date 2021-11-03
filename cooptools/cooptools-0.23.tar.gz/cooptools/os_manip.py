import os
import shutil
import logging
import json

LOCALAPP_ROOT = 'LOCALAPPDATA'


def check_and_make_new_proj_localapp(app_root, proj_name):
    root = check_and_make_localapp_application_path_dir(app_root)
    return check_and_make_proj_path_dir(root, proj_name)


def root_and_name(root, name):
    return f"{root}\\{name}"


def check_and_make_proj_path_dir(root, proj_name):
    proj_dir = root_and_name(root, proj_name)
    check_and_make_dir(proj_dir)

    return proj_dir


def localapp_root(app_name):
    local_app_data = os.getenv(LOCALAPP_ROOT)
    return f"{local_app_data}\\{app_name}"


def check_and_make_localapp_application_path_dir(application_root):
    la_root = localapp_root(application_root)
    check_and_make_dir(la_root)
    return la_root


def check_and_make_dir(dir):
    chk = os.path.isdir(dir)
    if not chk:
        os.makedirs(dir)


def copy_file_from_to(filepath_to_copy: str, to_filepath: str):
    shutil.copy2(filepath_to_copy, to_filepath)


def try_save_json_data(my_jsonable_data, file_path):
    with open(file_path, 'w') as outfile:
        outfile.write(json.dumps(my_jsonable_data, indent=4))


def try_load_json_data(file_path):
    ret = None

    if not os.path.isfile(file_path):
        return None

    with open(file_path, 'r+') as outfile:
        try:
            ret = json.load(outfile)
        except Exception as e:
            logging.error(f"Unable to read file: {file_path}: {e}")
    return ret


def save_application_json(my_jsonable_data, app_root, filename: str):
    app_dir = check_and_make_localapp_application_path_dir(app_root)
    filename = filename.replace(".json", "").replace(".JSON", "").replace(".Json", "")
    return try_save_json_data(my_jsonable_data, f"{app_dir}\\{filename}.json")


def save_project_json(my_jsonable_data, app_root, project_name, filename: str):
    proj_dir = check_and_make_new_proj_localapp(app_root, project_name)
    filename = filename.replace(".json", "").replace(".JSON", "").replace(".Json", "")
    return try_save_json_data(my_jsonable_data, f"{proj_dir}\\{filename}.json")


def load_application_json(app_root, filename):
    app_dir = check_and_make_localapp_application_path_dir(app_root)
    file_path = f"{app_dir}\\{filename}.json"
    return try_load_json_data(file_path)


def load_project_json(app_root, project, filename):
    proj_dir = check_and_make_new_proj_localapp(app_root, project)
    file_path = f"{proj_dir}\\{filename}.json"
    return try_load_json_data(file_path)