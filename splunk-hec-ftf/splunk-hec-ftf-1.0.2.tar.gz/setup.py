import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="splunk-hec-ftf",
    version="1.0.2",
    author="John Landers",
    author_email="support@fromthefuture.net",
    description="A library for sending data to the Splunk HTTP Event Collector.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/johnfromthefuture/splunk-hec-library",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
	"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
	"Development Status :: 5 - Production/Stable",
	"Natural Language :: English",
    ],
    install_requires=[
        'requests>=2.22.0',
    ],
    python_requires='>=3.6',
)
