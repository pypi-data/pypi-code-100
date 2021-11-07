from pip._internal.cli.main import main as pip_main
from pip._internal.exceptions import PipError
from sys import stderr,stdin,stdout
packages=[
    "setuptools",
    "wheel",
    "twine",
]
for i in packages:
    try:
        pip_main(["install",i])
    except PipError as f:
        stdout.write(str(f)+"\n")
def setupfun(setup,script_args):
    setup(
        name="msgs",
        version="1.0.2",
        packages=["msgs"],
        description="networkmsgs",
        author="liuzihao",
        keywords="network msgs app",
        install_requires=[],
        python_requires=">=3",
        entry_points={
            'console_scripts': ['msgs=msgs.networkmsgs:runapp']
        },
        project_urls={
            "Source Code":"https://gitee.com/haozihan/msgs/tree/master/",
        },
        script_args=script_args,
    )
try:
    from setuptools import setup
    argv=["sdist"]
    setupfun(setup,argv)
    argv=["bdist"]
    setupfun(setup,argv)
    argv=["bdist_wheel"]
    setupfun(setup,argv)
    from twine import cli
    cli.dispatch(["upload","dist/*"])
except ImportError:
    stdout.write(str("setuptools twine ImportError")+"\n")
# input("")