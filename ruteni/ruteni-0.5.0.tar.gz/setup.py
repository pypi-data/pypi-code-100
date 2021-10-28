import setuptools

# with open("README.md", "r") as fh:
#    long_description = fh.read()

setuptools.setup(
    name="ruteni",
    version="0.5.0",
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
        "": ["resources/*", "templates/*", "static/*", "static/*/*", "static/*/*/*"]
    },
    install_requires=[
        "aiodns",
        "aioredis",
        "aiosmtplib",
        "aiosmtpd",
        "anyio",
        "apscheduler",
        "argon2_cffi",
        "authlib",
        "babel",
        "databases",
        "httpx",
        "itsdangerous",
        "jinja2",
        "jwcrypto",
        "limits",
        "python-multipart",
        "paramiko",
        "python-socketio",
        "pyrfc3339",
        "sqlalchemy",
        "sqlalchemy-utils",
        "starlette",
        "transitions",
        "websockets",
        "zxcvbn",
    ],
    test_suite="tests.build_test_suite",
)
