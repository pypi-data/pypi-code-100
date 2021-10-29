import os
from setuptools import setup

version = "1.0.0.alpha14"

APPLICATION_WEBSITE_STR = "https://gitlab.com/SunyataZero/website-generator"
# APPLICATION_NAME_STR = "Website Generator"
PROJECT_NAME_STR = "website-generator"
PACKAGE_NAME_STR = "websitegen"
SCRIPT_NAME_STR = "website-gen"
SHORT_DESCRIPTION_STR = "A minimalistic static website generator"
SETTINGS_STR = "settings.ini"

long_description_str = ""
this_dir_abs_path_str = os.path.dirname(__file__)
readme_abs_path_str = os.path.join(this_dir_abs_path_str, "README.md")

try:
    with open(readme_abs_path_str, "r") as file:
        long_description_str = '\n' + file.read()
except FileNotFoundError:
    pass

setup(
    name=PROJECT_NAME_STR,
    version=version,
    packages=[PACKAGE_NAME_STR],
    url=APPLICATION_WEBSITE_STR,
    license='GPLv3',
    author='Tord Dellsén',
    author_email='tord.dellsen@gmail.com',
    description=SHORT_DESCRIPTION_STR,
    install_requires=["mistletoe>=0.7.2"],
    include_package_data=True,
    entry_points={"console_scripts": [f"{SCRIPT_NAME_STR}={PACKAGE_NAME_STR}.main:main"]},
    long_description_content_type='text/markdown',
    long_description=long_description_str,
    python_requires='>=3.9',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Development Status :: 2 - Pre-Alpha'
    ]
)
