import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TournamentFetcher",
    version="0.2.1",
    author="Impasse52",
    description="A Challonge and Smash.gg API wrapper with pandas support.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Impasse52/TournamentFetcher",
    packages=setuptools.find_packages(),
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
)

# py -m build; twine upload --skip-existing dist/*; pip install .