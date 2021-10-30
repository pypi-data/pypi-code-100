import setuptools

with open("README.md", "r") as fh:
    description_lines = fh.readlines()
    description_lines = [line for line in description_lines if not "<img src=" in line]
    long_description = "\n".join(description_lines)

setuptools.setup(
    name="playsh",
    version="0.0.2",
    url="https://github.com/panmar/playsh",
    author="Marcin Panasiuk",
    author_email="panasiuk.marcin@gmail.com",
    description="A playground for OpenGL fragment shader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    install_requires=["injector", "glfw", "PyOpenGL", "PyGLM", "numpy", "pillow"],
    extras_require={"dev": ["black", "mypy"]},
)
