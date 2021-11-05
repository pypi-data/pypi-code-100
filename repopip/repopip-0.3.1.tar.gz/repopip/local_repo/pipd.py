from pathlib import Path
from os import environ
import subprocess

USER_CONFIG_FOLDER = Path(environ['HOME']).joinpath('.config')
PACKAGES_CONTAINER_FOLDER = Path(__file__).parent.joinpath('static', 'simple')
PIP_CONFIG_FOLDER = USER_CONFIG_FOLDER.joinpath('pip')
PIP_CONFIG_FILE = PIP_CONFIG_FOLDER.joinpath('pip.conf')

class PipConfEditor:

    def areStructuresCreated(self):
        return PIP_CONFIG_FOLDER.exists() and PIP_CONFIG_FILE.exists()

    def mkStructures(self):
        if(not PIP_CONFIG_FOLDER.exists()):
            PIP_CONFIG_FOLDER.mkdir()
        if(not PIP_CONFIG_FILE.exists()):
            open(PIP_CONFIG_FILE.absolute(), 'w').close()

    def configForLocal(self):
        with PIP_CONFIG_FILE.open('w') as f:
            f.writelines(['[global]\n', 'index-url=http://127.0.0.1:5000/'])

    def configForDefault(self):
        with PIP_CONFIG_FILE.open('w') as f:
            f.close()

class PipManager:

    def downloadPakage(self, *args):
        comand = ['pip3', 'download']
        comand.extend(args)
        output = subprocess.run(comand, cwd=PACKAGES_CONTAINER_FOLDER, capture_output=True, text=True)
        return output.stdout

# conf = PipConfEditor()
# conf.configForLocal()

# manager = PipManager()
# print(manager.downloadPakage('click'))
