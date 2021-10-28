import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

#with open("requirements.txt") as f:
#    requireds = f.read().splitlines()

setup(
    name="rembg_cars",
    version="1.0.3",
    description="Remove image background from cars",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/poropeza/rembg_cars",
    author="Peter Oropeza",
    author_email="peteroropeza2@gmail.com",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="remove, background, u2net",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8, <4",
    install_requires=[            # I get to this in a second
          'flask>=1.1.2',
          'numpy>=1.19.5',
          'pillow>=8.0.1',
          'scikit-image>=0.17.2',
          'torch>=1.9.1',
          'torchvision>=0.10.1',
          'waitress>=1.4.4',
          'tqdm>=4.51.0',
          'requests>=2.24.0',
          'scipy>=1.5.4',
          'pymatting>=1.1.1',
          'filetype>=1.0.7'
      ],
    entry_points={
        "console_scripts": [
            "rembg=rembg.cmd.cli:main",
            "rembg-server=rembg.cmd.server:main",
        ],
    },
)