import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
      long_description = fh.read()

setuptools.setup(
      name='pyzon',
      version='0.0.2',
      description='Some python utils includes The Zen of Python',
      url='https://github.com/nzooherd/pyzon',
      author='nzooherd',
      author_email="nzooherd@gmail.com",
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ],
      package_dir={"": "src"},
      packages=setuptools.find_packages(where="src"),
      python_requires=">=3.6",
)