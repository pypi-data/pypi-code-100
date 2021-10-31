import setuptools

install_requirements = [
    'matplotlib',
    'python-docx'
]

test_requirements = [
    'hypothesis',
    'pytest'
]

SHORT_DESCRIPTION = 'Utilities for visualizing and publishing research data'
LONG_DESCRIPTION = SHORT_DESCRIPTION

setuptools.setup(
    name='python-playfair',
    version='0.1',
    description='Utilities for visualizing and publishing research',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url='http://github.com/tmbb/playfair',
    project_urls={
        "Bug Tracker": "https://github.com/tmbb/playfair/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"playfair": "src"},
    author='Tiago Barroso',
    author_email='tmbb@campus.ul.pt',
    license='MIT',
    install_requires=install_requirements,
    test_requires=test_requirements,
    packages=setuptools.find_packages(where="src"),
    package_data={
        "": ["*.docx"]
    },
    zip_safe=False
)
