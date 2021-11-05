import setuptools.command.build_py
from setuptools import find_packages

reqs = [
"Click==7.1.2",
"cycler==0.10.0",
"kiwisolver==1.1.0",
"matplotlib",
"numpy",
"pyparsing==2.4.0",
"PyQt5",
"PyQt5-sip",
"python-dateutil==2.8.0",
"python-dotenv==0.10.1",
"six==1.12.0",
"resources",
"jinja2",
"Flask==1.1.1",
"flask_nav",
"requests~=2.25.1",
"pandas~=1.1.4",
"mpld3~=0.5.2",
"markupsafe~=1.1.1",
"setuptools~=49.6.0",
"pip~=20.2.4"
]


with open("README.md", "r") as fh:
    long_description = fh.read()
    fh.close()

setuptools.setup(
    install_requires=reqs,
    name='titania',
    version='0.3.5',
    author="Maciej Majewski",
    author_email="mmajewsk@cern.ch",
    description="Titania monitoring framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/mmajewsk/titania",
    package_dir={'titania': 'titania', 'resources': 'titania/resources'},
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_data={'':['*.css', '*.gif', '*.png']},
    # data_files=[('titania',['requirements.txt'])],
    include_package_data=True,

)
