import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ncspy",
    version="0.2.2",
    author="Vincy.zsh",
    author_email="Vincysuper07@gmail.com",
    description='A NoCopyrightSounds "API" wrapper written with asyncio.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Vincydotzsh/pyncs",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=["aiohttp", "beautifulsoup4", "slimit"],
    packages=["ncs"],
    python_requires=">=3.7",
)
