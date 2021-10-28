from setuptools import setup, find_packages

setup(
	name="roboid",
	version="1.5.17",
	author="Kwang-Hyun Park",
	author_email="akaii@kw.ac.kr",
	description="Python Package for Hamster, Hamster-S, Turtle, Albert Ai, and Zerone",
	long_description=open("README.md").read(),
	long_description_content_type="text/markdown",
	install_requires=["pyserial", "websocket-client"],
	packages=find_packages(exclude=["examples", "tests"]),
	python_requires=">=3",
	zip_safe=False,
	classifiers=[
		"License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)"
	]
)