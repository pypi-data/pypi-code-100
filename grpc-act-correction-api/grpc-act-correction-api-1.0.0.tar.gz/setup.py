import setuptools

# read the contents of README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="grpc-act-correction-api",
    version="1.0.0",
    author="lgalkina",
    author_email="liudmila.galkina@gmail.com",
    description="GRPC python client for act-correction-api",
    url="https://github.com/ozonmp/act-correction-api",
    packages=setuptools.find_packages(),
    python_requires='>=3.5',
    long_description=long_description,
    long_description_content_type='text/markdown'
)