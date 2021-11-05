from setuptools import setup, find_packages
import pathlib


HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text(encoding="utf8")

setup(
	name="Justify_discord",
	version="1.0",
	author="MagMigo / Reidy",
	description="Discord bot util",
	long_description=README,
	long_description_content_type="text/markdown",
	url="https://github.com/MagM1go/Justify",
	packages=find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3.10",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.7',
)