import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="meduse-CERTIC",
    version="0.0.2",
    author="Mickaël Desfrênes",
    author_email="mickael.desfrenes@unicaen.fr",
    description="Outil en ligne de commande destiné à réaliser des copies statiques des projets du Pôle Document Numérique.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.unicaen.fr/pdn-certic/advStatificator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "sanic",
        "lxml",
        "argh",
        "requests",
        "beautifulsoup4",
        "elasticsearch>=6.0.0,<7.0.0",
    ],
    python_requires=">=3.6",
    include_package_data=True,
    entry_points={
        "console_scripts": ["meduse=meduse.__main__:run_cli"],
    },
)
