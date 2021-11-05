import argparse
import os
from PyInquirer import prompt

from .api import Gitlab
from .screens import ProjectsScreen, Screen

def ask_for_token():
    Screen(None).clear_screen()
    token = None
    question = [{
        'type': 'password',
        'name': 'token',
        'message': 'Input your token (you can also use -t/--token)',
    }]
    answer = prompt(questions = question)
    if answer != {} and answer["token"] != "":
        token = answer["token"]
    Screen(None).clear_screen()
    return token

def ask_for_gid():
    Screen(None).clear_screen()
    token = None
    question = [{
        'type': 'input',
        'name': 'gid',
        'message': 'Input the group id (you can also use -g/--group-id)',
    }]
    answer = prompt(questions = question)
    if answer != {} and answer["gid"] != "":
        token = answer["gid"]
    Screen(None).clear_screen()
    return token

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token', help = 'Token de GitLab', required=False)
    parser.add_argument('-g', '--group-id', help = 'ID del grupo', required=False)
    args = vars(parser.parse_args())

    if args["token"] == None:
        new_token = ask_for_token()
        if new_token == None:
            parser.print_help()
            print("Error: You havent provide a token by cli or by typing it.")
            exit(1)
    if args["group_id"] == None:
        new_gid = ask_for_gid()
        if new_gid == None:
            parser.print_help()
            print("Error: You havent provide a group id by cli or by typing it.")
            exit(1)

    gl = Gitlab(gitlab_url = "https://gitlab.com/", group_id = args["group_id"], token = args["token"])
    gl.start()
    screen = ProjectsScreen(gl)
    screen.run()
    gl.stop()
    exit(0)