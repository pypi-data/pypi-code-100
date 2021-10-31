from setuptools import setup, find_packages

VERSION = '0.9.1'
DESCRIPTION = 'The open-world, OpenGL video game made in Python'
LONG_DESCRIPTION = 'The open-world, OpenGL video game made in Python, this project is still in development, but feel free to give it a go!'

# Setting up
setup(
    name="Python-Pycraft",
    version=VERSION,
    author="PycraftDev (Tom Jebbo)",
    author_email="<thomasjebbo@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open("README.md", "r").read(),
    packages=find_packages(),
    install_requires=["Pillow", "Pygame", "PyOpenGL", "PyOpenGL-Accelerate", "Numpy", "PyAutoGUI", "Psutil", "PyWaveFront", "Py-Cpuinfo", "Gputil", "Tabulate"],
    keywords=['python', "pillow", "pygame", "pyopengl", "pyopengl-accelerate", "numpy", "gputil" "py-cpuinfo", "pywavefront", "psutil", "pyautogui", "tabulate", "OpenGL", "khronos", "pycraftDev", "game", "3D", "Openworld"],
    classifiers=[
        "Intended Audience :: Other Audience",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Topic :: Games/Entertainment"
    ]
)