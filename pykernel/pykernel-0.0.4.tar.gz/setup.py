from setuptools import setup
setup(
    name="pykernel",
    version="0.0.4",
    description="Python & text Windows CMD Editior written with only native libaries",
    py_modules=["pykernel"],
    package_dir={"":"code"},
    url="https://github.com/coolnicecool/Pykernel",
    author="Raleigh Priour"
)
#python setup.py build
#python setup.py sdist bdist_wheel
#twine upload dist/*
