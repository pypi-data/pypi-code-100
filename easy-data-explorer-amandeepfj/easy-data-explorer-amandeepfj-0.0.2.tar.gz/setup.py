import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'Easy Data Explorer'
LONG_DESCRIPTION = 'Python library to do common data exploring tasks.'

# Setting up
setuptools.setup(
    name="easy-data-explorer-amandeepfj",
    version=VERSION,
    author="amandeepfj (Amandeep Jiddewar)",
    author_email="<amandeep.jiddewar@alumni.emory.edu>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/amandeepfj/easy_data_explorer",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=['pandas', 'numpy'],
    keywords=['python', 'data explore'],
    project_urls={
        "Bug Tracker": "https://github.com/amandeepfj/easy_data_explorer/issues",
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)