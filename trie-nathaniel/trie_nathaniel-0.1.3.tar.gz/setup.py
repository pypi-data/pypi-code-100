from setuptools import setup, find_packages

with open("README.md", "r") as f:
    ld = f.read()

with open("requirements.txt", "r") as f:
    rq = f.read().splitlines()

setup(
    name='trie_nathaniel',
    version='0.1.3',
    description='Calls commands to the trie server that can modify its state',
    python_requires='>=3.6, < 3.10',
    install_requires=rq,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    author='Nathaniel Thomas',
    author_email='catchnate+pypi@gmail.com',
    py_modules=["triecli", "cli"],
    license='MIT',
    url='https://github.com/Nathaniel-github/TrieCLI',
    long_description=ld,
    long_description_content_type='text/markdown',
    entry_points={
        "console_scripts": [
            "triecli=triecli:cli",
        ]
    },

    classifiers=[
        "Development Status :: 6 - Mature",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8"
    ]
)
