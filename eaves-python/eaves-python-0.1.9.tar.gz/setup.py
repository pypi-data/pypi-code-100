import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="eaves-python",
	version="0.1.9",
	author="coverosu",
	author_email="coverosu@gmail.com",
	description="Wrapper around pygame cause why NOT",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/coverosu/eaves",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.9',
)