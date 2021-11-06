from setuptools import setup, find_packages

setup_args = dict(
    name = 'justanunsuspiciousmodule',
    version = '1.2',
    description='Class with a module for lab',
    license='MIT',
    packages=find_packages(),
    author = 'Mekatto', 
    author_email = 'igor@mekatto.com',
    url = 'https://github.com/Igor-Sviridov/justanunsuspiciousmodule',
    download_url = 'https://pypi.org/project/justanunsuspiciousmodule/',
    python_requires='>3.6.0',
)

install_requires = [
          'ipywidgets',
          'numpy',
          'matplotlib',
          'scikit-commpy'


]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
