import subprocess
import os
from sys import version_info
MAJOR=3
MINOR=1
PATCH=0
VERSION="{MAJOR}.{MINOR}.{PATCH}".format(MAJOR=MAJOR, MINOR=MINOR, PATCH=PATCH)

ADVANCED_VERSION = VERSION
BRANCH="master"
COMMIT=None
AHEAD=0
ADVANCED_SET=False

def get_more_info():
    global BRANCH
    global COMMIT
    global AHEAD
    global ADVANCED_SET
    source_dir = os.path.dirname(os.path.realpath(__file__))
    old_cwd = os.getcwd()
    try:
        os.chdir(source_dir)
        response = mod_string(
                subprocess.check_output(["git", "describe", "--long"], 
                                         stderr=subprocess.STDOUT)).strip()
        tag, ahead, commit = response.split("-")
        AHEAD = ahead
        COMMIT = commit
        branch = mod_string(
                subprocess.check_output(["git", "rev-parse",
                                         "--abbrev-ref", "HEAD"])).strip()
        BRANCH = branch
        ADVANCED_SET = True
    except subprocess.CalledProcessError as e:
        pass
    finally:
        os.chdir(old_cwd)

def get_version():
    global ADVANCED_VERSION
    get_more_info()
    ADVANCED_VERSION ="{vers}-{ahead}-{commit}-{branch}".format(
            vers=VERSION, ahead=AHEAD, 
            commit="release_commit" if COMMIT is None else COMMIT,
            branch=BRANCH)
    return ADVANCED_VERSION


def mod_string(string):
    if (version_info > (3, 0)):
        return string.decode()
    else:
        return string



