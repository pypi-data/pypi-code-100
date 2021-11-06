import setuptools

setuptools.setup(
    name="akilan",
    version="0.0.1",
    author="AKilan km",
    description="Image classification engine",
    packages=["ICE"],
    install_requires=["numpy", "sklearn", "matplotlib", "pandas"],
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
