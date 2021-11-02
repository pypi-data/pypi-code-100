#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
"""
B→FeelLog - 2021 - por jero98772
B→FeelLog - 2021 - by jero98772
"""
from core.tools.webutils import genTokenFile
from setuptools import setup, find_packages
setup(
	name='B-FeelLog',
	version='1.0.1',
	license='GPLv3',
	author_email='jero98772@protonmail.com',
	author='jero98772',
	description='free source minimal multilingual blog maker and manager for different blog entries and multiple blog entries , with web interface. in this blog can use images but we looking to keep it minimalism.',
	url='https://jero98772.pythonanywhere.com/',
	packages=find_packages(),
    install_requires=['Flask','deep-translator'],
    include_package_data=True,
    long_description="""# B-FeelLog\n', '\n', '![logo](https://github.com/jero98772/B-FeelLog/blob/main/docs/Screenshots/B-feelog_logo1.jpg?raw=true)\n', '\n', '\t\tBlog feel-log ,feel Blog   \n', '\n', 'free source minimal multilingual blog maker and manager for different blog entries and multiple blog entries , with web interface. in this blog can use images but we looking to keep it minimalism.\n', '\n', 'now is bilingual with support in \n', '- Spanish \n', '- English\n', '- German\n', '- Basque\n', '- Italian\n', '- Russian\n', '\n', '**more information** [here](https://github.com/jero98772/B-FeelLog/blob/main/docs/FAQs.md)\n', '\n', '**video tutorial** [here](https://vimeo.com/manage/videos/580068235)\n', '\n', 'please report some issues or if you need help \n', '### Made for:\n', 'manage a blog ,sharing and proposing a tool for expressing\n', '\n', '### Download \n', 'Download repo\n', '\n', '\tgit clone https://github.com/jero98772/B-FeelLog.git\n', '### Update\n', 'run in repo folder\n', '\n', '\tgit pull\n', '\n', '### Install\n', '\n', 'run install : \n', '\n', '\tpython setup.py install\n', '\n', '### Usage \n', '\n', 'the app run in [localhost:9600](http://localhost:9600/this.html)\n', 'remember you need authenticate in [localhost:9600/blog/< TOKEN >/](localhost:9600/this/defaulttoken/)\n', 'the initial token is:\n', '\t\n', '\tdefaulttoken\n', '\n', '### Screenshots\n', '![main](https://github.com/jero98772/B-FeelLog/blob/main/docs/Screenshots/2021-05-06-185257_770x321_scrot.png)\n', '![flex blog](https://github.com/jero98772/B-FeelLog/blob/main/docs/Screenshots/2021-05-06-165512_752x551_scrot.png)\n', '![translation](https://github.com/jero98772/B-FeelLog/blob/main/docs/Screenshots/2021-05-07-203242_822x595_scrot.png)\n""",
    long_description_content_type='text/markdown',
	)
genTokenFile("data/token.txt")