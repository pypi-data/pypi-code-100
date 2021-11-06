import setuptools
from pathlib import Path

# with open("README.md", "r") as fh:
#    long_description = fh.read()

setuptools.setup(
    name="ruteni",
    version="0.6.0",
    author="Johnny Accot",
    description="Thin layer over Starlette",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    py_modules=["ruteni"],
    package_data={
        "ruteni": [
            str(path).replace("ruteni/dist", "dist")
            for path in Path("ruteni/dist").glob("**/*")
        ],
        "": ["resources/*", "templates/*"],
    },
    install_requires=[
        "aiodns",
        "aioredis",
        "aiosmtplib",
        "aiosmtpd",
        "aiosqlite",
        "anyio",
        "apscheduler",
        "argon2_cffi",
        "authlib",
        "babel",
        "boolean.py",
        "databases",
        "html5lib",
        "httpx",
        "itsdangerous",
        "jinja2",
        "jwcrypto",
        "limits",
        "marshmallow",
        "python-multipart",
        "paramiko",
        "pillow",
        "python-socketio",
        "pyrfc3339",
        "sqlalchemy",
        "sqlalchemy-utils",
        "starlette",
        "tabulate",
        "totates",
        "transitions",
        "urlobject",
        "uvicorn",
        "webcolors",
        "websockets",
        "werkzeug",
        "zxcvbn",
    ],
    test_suite="tests.build_test_suite",
)
