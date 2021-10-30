import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="photon-lang",
    version="0.0.1",
    packages=setuptools.find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    #package_data={
    #    'photon-lang':['templates/*.py']
    #},
    python_requires='>=3.6',
    install_requires=[]
)
