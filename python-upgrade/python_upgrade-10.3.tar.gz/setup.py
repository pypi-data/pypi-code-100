from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="python_upgrade",
    version="10.3",
    author="ZetaMap",
    description="Un module python contenant des fonctions plus avancées. Je l'ai conçu principalement pour la Numworks car elle n'a pas beaucoup de librairie.",
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/ZetaMap/Python_Upgrade",
    project_urls={
        "GitHub Project": "https://github.com/ZetaMap/Python_Upgrade",
        "My GitHub Page": "https://github.com/ZetaMap/"
    },
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
)
