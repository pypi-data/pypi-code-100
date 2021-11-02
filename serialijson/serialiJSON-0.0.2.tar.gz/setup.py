import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="serialiJSON",
	version="0.0.2",
	author="Matías Del Pin",
	author_email="madelpin@protonmail.com",
	description="A simple converter from complex objects to JSON",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url= 'https://github.com/matias-alejandro/serialiJSON',
	project_urls={
		'Source': 'https://github.com/matias-alejandro/serialiJSON',
		'Tracker': 'https://github.com/matias-alejandro/serialiJSON/issues',
	},
	package_dir={"": "src"},
	packages=setuptools.find_packages(where="src"),
	key_words='converter toJSON complex object base class',
	classifiers=[
		"Programming Language :: Python",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
		"Topic :: Software Development :: Libraries :: Python Modules"
	],
	python_requires='>=2.7'
)
