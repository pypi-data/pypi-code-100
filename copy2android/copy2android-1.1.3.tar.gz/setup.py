import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="copy2android",
    version="1.1.3",
    author="loyal888",
    author_email="h916232476@gmail.com",
    description="Copy From Mac,Paste On Android",
    long_description="Copy From Mac,Paste On Android",
    long_description_content_type="text/markdown",
    url="https://github.com/loyal888/copy2android",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
