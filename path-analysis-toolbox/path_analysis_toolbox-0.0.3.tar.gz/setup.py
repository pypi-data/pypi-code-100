import setuptools

VERSION = "0.0.3"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="path_analysis_toolbox",
    version=VERSION,
    author="Kamila Sproska",
    author_email="kamila.sproska@gmail.com",
    description="Toolbox for various path analysis and creating directories.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['path', 'directory', 'filename', 'extension', 'create'],
    url="https://github.com/ksproska/path_analyser",
    packages=setuptools.find_packages()
)
