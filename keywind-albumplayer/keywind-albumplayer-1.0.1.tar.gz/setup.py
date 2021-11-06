import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
	long_description = fh.read()
setuptools.setup(
	name="keywind-albumplayer",
	version="1.0.1",
	author="Keywind",
	author_email="keywind127@gmail.com",
	description="Installing this package will allow you to play music albums.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/keywind1207/keywind-albumplayer",
	project_urls={
		"Bug Tracker": "https://github.com/keywind1207/keywind-albumplayer/issues",
	},
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	package_dir={"": "src"},
	packages=setuptools.find_packages(where="src"),
	python_requires=">=3.6",
	
	install_requires=[
		'markdown',
		'pynput',
		'wave',
		'pyaudio'
	]
	
)