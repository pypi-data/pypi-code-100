# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['audio_program_generator']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0',
 'gTTS>=2.2.2,<3.0.0',
 'pydub>=0.25.1,<0.26.0',
 'single-source>=0.2.0,<0.3.0',
 'tqdm>=4.61.0,<5.0.0']

entry_points = \
{'console_scripts': ['apg = audio_program_generator.apg:main']}

setup_kwargs = {
    'name': 'audio-program-generator',
    'version': '1.7.0.0',
    'description': 'Create an audio program from a text file containing English sentences',
    'long_description': '\n[![Python package](https://github.com/jeffwright13/audio_program_generator/actions/workflows/python-package.yml/badge.svg)](https://github.com/jeffwright13/audio_program_generator/actions/workflows/python-package.yml)\n\n# apg (audio_program_generator)\nGenerates an audio program from text, with option to mix in background sound\n\nPossible use cases:\n- make your own yoga or qi gong routine\n- play a list of daily affirmations\n- meditate to a mantra with drone music in the background\n- create an audio book\n- read a kid a bedtime story without actually having to do the reading\n\n# Prerequisites\n* Python (3.7+) [*note to mac users: your system may be using Python 2.7 by default. To find out, issue the command `python --version`. If your system shows anything less than 3.7, make sure you create a virtual environment before installing this package (see Installation section below)*]\n* [pip](https://pypi.org/project/pip/) (option 1)\n* [git](https://git-scm.com/) + [poetry](https://python-poetry.org/) (option 2)\n* Local installation of [ffmpeg](https://www.ffmpeg.org/)\n\n# Installation & Execution\n## With `pip`:\n- Create a virtual environment and activate it:\n    - `python -m venv venv`\n    - `source ./venv/bin/activate`\n - Install the package:\n    - `pip install audio-program-generator`\n- Once this is done, you will have an "apg" executable available in your terminal. You can type `apg` for basic help, or `apg --help` for full instructions.\n- Deactivate your virtual environment when finished:\n    - `deactivate`\n\n## With `poetry`:\n- Clone the repo and cd into the directory:\n    - `git clone https://github.com/jeffwright13/audio_program_generator.git`\n    - `cd audio_program_generator`\n- Install the dependencies using poetry, and activate the virtual environment:\n    - `poetry install --no-dev`\n    - `poetry shell`\n- Once this is done, you will have an "apg" executable available in your terminal. You can type `apg` for basic help, or `apg --help` for full instructions.\n- Exit the poetry virtual environment when finished:\n    - `exit`\n\n## With `docker`:\n- Clone the repo and cd into the directory:\n    - `git clone https://github.com/jeffwright13/audio_program_generator.git`\n    - `cd audio_program_generator`\n- Execute `make build` (builds Docker image)\n- Execute `make run` (runs container and enters in `poetry` shell, ready to run `apg` executable\n- Results from `make run` will be available locally in the `/apgfiles` folder, even after the container is stopped\n\n## With `flask`:\n- There is a [sister project](https://github.com/jeffwright13/apg_flask) that wraps the apg module in a bare-bones Flask app. This can be hosted locally, or in a cloud provider such as Heroku, Digital Ocean, or AWS. This method is considered experimental at the moment, and is not officially supported.\n\n# Usage\n*Assumes you are using the provided `apg` command line interface, installed with one of the methods above*\n- Populate a semicolon-separated text file with plain-text phrases, each followed by an inter-phrase duration (see example below). Each line of the file is comprised of:\n   - a phrase to be spoken (in English)\n   - a semicolon\n   - a silence duration (in seconds)\n- Provide a sound file for background sound (optional)\n- Execute the command in your terminal: `apg [options] <phrase_file> [sound_file]`\n\nThe script will generate and save a single MP3 file. The base name of the MP3 file is the same as the specified input file. For example, if the script is given input file "phrases.txt", the output file will be "phrases.mp3". It will be saved to the same folder that the input text file was taken from.\n\nThe optional `[sound_file]` parameter, when specified, is used to mix in background sounds/music. This parameter specifies the path/filename of the sound file to be mixed in with the speech generated from the phrase file. If the sound file is shorter in duration than the generated speech file, it will be looped. If it is longer, it will be truncated. The resulting background sound (looped or not) will be faded in and out to ensure a smooth transition (6 seconds at beginning and en). Currently, only .wav files are supported as inputs.\n\nThe `--attenuation` option allows fine-tuning the background sound level so it doesn\'t drown out the generated speech.\n\nThe `--slow` option generates each speech snippet is a slow-spoken style.\n\nThe `--tld` option allows the user to select one of several regional \'accents\' (English only). For accents, select one from the following list: ["com.au", "co.uk", "com", "ca", "co.in", "ie", "co.za"]\n\nSpecifying option `--book-mode` creates a spoken-word program (with or without background soundfile). It does this by reading in a file that does not have inter-phrase durations inserted, as is normally the case. This feature is new and needs some tweaking. For now, just make sure your input file is pure text, and experiement with using a single line (with many sentences) as one paragraph vs. multiple lines, one per sentence. You wil notice a difference in how the \'speaker\' pauses between phrases.\n\nThe CLI prints out a progress bar as the phrase file is converted into speech snippets. No progress bar is shown for the secondary mix step. There may be a significant delay in going from the end of the first stage (snippet generation) to the end of the second stage (mixing), primarily because of reading in the .wav file, which may be large. For this reason, you may want to select a sound file for mixing that is small (suggested <20MB). Otherwise, be prepared to wait. The progress bar may be disabled with the `--no-progress-bar` option.\n\n# Example <phrase_file> format:\n    Phrase One;2\n    Phrase Two;5\n    Phrase Three;0\n\n# Example `--book-mode` file format:\n    Here we have sentence number one. It\'s a lovely sentence, and deserves its own paragraph.\n    Here is a second paragraph, and this is sentence number one (again) in that paragraph. And this is sentence number two! Then shalt thou count to three - no more, no less. Three shall be the number thou shalt count, and the number of the counting shall be three. Four shalt thou not count, neither count thou two, excepting that thou then proceed to three. Five is right out. Once the number three, being the third number, be reached, then lobbest thou thy Holy Hand Grenade of Antioch towards thy foe, who, being naughty in my sight, shall snuff it.\n\n# Author:\nJeff Wright <jeff.washcloth@gmail.com>\n\n# Collaborators:\nBob Belderbos\nErik OShaughnessy\n',
    'author': 'Jeff Wright',
    'author_email': 'jeff.washcloth@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jeffwright13/audio_program_generator/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
