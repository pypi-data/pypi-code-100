import argparse
from time import sleep

from .api import Gitlab
from .screens import ProjectsScreen

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token', help = 'Token de GitLab', required=True)
    parser.add_argument('-g', '--group-id', help = 'ID del grupo', required=True)
    args = vars(parser.parse_args())

    gl = Gitlab(gitlab_url = "https://gitlab.com/", group_id = args["group_id"], token = args["token"])
    gl.start()
    screen = ProjectsScreen(gl)
    screen.run()