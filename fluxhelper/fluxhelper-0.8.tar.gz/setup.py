from distutils.core import setup
setup(
    name="fluxhelper",
    packages=["fluxhelper", "fluxhelper.jarvis"],
    version="0.8",
    license="MIT",
    description="Helper library made for my projects",
    author="Philippe Mathew",
    author_email="philmattdev@gmail.com",
    url="https://github.com/bossauh/fluxhelper",
    download_url="https://github.com/bossauh/fluxhelper/archive/refs/tags/v_08.tar.gz",
    keywords=["helper"],
    install_requires=[
        "pycaw",
        "termcolor",
        "flask",
        "python-dateutil",
        "requests",
        "pymongo",
        "dnspython",
        "montydb",
        "aiohttp",
        "motor"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ]
)
