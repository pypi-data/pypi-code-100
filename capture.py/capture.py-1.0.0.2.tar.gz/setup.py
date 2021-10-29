import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
setup(
    name="capture.py",
    version="1.0.0.2",
    url="https://github.com/SirLez",
    download_url="https://github.com/SirLez/capture.py/archive/refs/heads/main.zip",
    description="Capture chat app Bots with python!",
    long_description=README,
    long_description_content_type="text/markdown",
    author="SirLez",
    author_email="SirLezDV@gmail.com",
    license="MIT",
    keywords=[
        'capture',
        "capture.py",
        "capture.chat",
        "capture-chat",
        'captureS',
        'capture-bot',
        'capture-chat',
        'capture-lib',
        'cptr',
        'cptr.co',
        "SirLez",
        "sirlez",
        "srlz",
        "SrLz",
        'api',
        'python',
        'python3',
        'python3.x',
        'api',
        'python',
        'python3',
        'python3.x'
    ],
    include_package_data=True,
    install_requires=[
        'requests',
        "sseclient==0.0.6"
    ],
    setup_requires=[
        'wheel'
    ],
    packages=find_packages(),
)