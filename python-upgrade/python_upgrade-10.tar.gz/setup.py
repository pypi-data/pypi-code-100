from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="python_upgrade",
    version="10",
    author="ZetaMap",
    description="A small module allowing to link the kandinsky module, from the Numworks, to a window.",
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
