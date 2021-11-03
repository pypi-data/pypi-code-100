from setuptools import setup

# with open("README.md", "r") as f:
#   long_description = f.read()

setup(
  name='containerplus',
  version='1.0.3',
  description="More containers and various container utils",
  packages=["container"],
  package_dir={"": "src"},
  # long_description=long_description,
  # long_description_content_type="text/markdown",
  url="https://github.com/MasterCoder21/container",
  author="minecraftpr03",
  author_email=None,
  classifiers=[
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent"
  ]
)