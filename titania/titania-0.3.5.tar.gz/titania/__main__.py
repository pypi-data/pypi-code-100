import argparse
import os
from pathlib import Path

from titania.example.example_files_interior import config_file, main_file, control_panel_file, thresholds_file, \
    thresholds_tab_file


def create_python_file_and_fill(path, file_input):
    os.mknod(path)
    file = open(path, "w")
    file.write(file_input)
    file.close()


if __name__=="__main__":
    print("Creation start")
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('subprogram', type=str, help='start new project')
    parser.add_argument('-n', '--name', type=str)


    args = parser.parse_args()
    destination = Path(os.getcwd())
    dirname = destination/args.name
    if args.subprogram in ["start", "add"]:
        os.mkdir(dirname)
        os.mknod(dirname/"__init__.py")

        for folder in ["data","panels","plots","views"]:
            os.mkdir(dirname/folder)
            os.mknod(dirname/folder/"__init__.py")

        create_python_file_and_fill(dirname / "panels/control_panel.py", control_panel_file())
        create_python_file_and_fill(dirname / "views/thresholds.py", thresholds_file())
        create_python_file_and_fill(dirname / "views/thresholds_gui.py", thresholds_tab_file())

    if args.subprogram == "start":
        create_python_file_and_fill(dirname / "config.py", config_file(args.name))
        create_python_file_and_fill(dirname / "main.py", main_file(args.name))
    print("Creation finished")
