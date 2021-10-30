from setuptools import setup, find_packages
import pathlib


HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text(encoding="utf8")

setup(
	name="Loli-wrapper",
	version="1.0.4",
	author="MagMigo",
	description="Simple wrapper for loli api.",
	long_description=README,
	long_description_content_type="text/markdown",
	url="https://loli-api.ml",
	packages=find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3.10",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.7',
)
