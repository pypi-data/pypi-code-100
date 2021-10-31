import setuptools
with open("README.md", "r") as f:
	long_description = f.read()

requirements = [
	"discord",
	"discord.py[voice]",
	"discord_components",
	"youtube_dl",
	"datetime",
	"requests"
]

setuptools.setup(
	name = "aoku",
	version = "2.1.2",
	author = "AineD3V",
	author_email = "priskozena@gmail.com",
	description = "The package for writing your own discord bot",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	url = "https://aokuapi.herokuapp.com/",
	packages = setuptools.find_packages(),
	install_requires = requirements,
	classifiers=[
		"Programming Language :: Python :: 3.8",
		"License :: OSI Approved :: GNU General Public License (GPL)",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)