import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="amcache2",
    version="0.1.3",
    author="Jan Starke",
    author_email="jan.starke@t-systems.com",
    description="creates a bodyfile from AmCache.hve",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/janstarke/amcache2.py",
    project_urls={
        "Bug Tracker": "https://github.com/janstarke/amcache2.py/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires = [
        "regipy"
    ],
    scripts=['src/amcache2.py']
)