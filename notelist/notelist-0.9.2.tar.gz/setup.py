"""Notelist Setup script."""

import setuptools as st


if __name__ == "__main__":
    # Long description
    with open("README.md") as f:
        long_desc = f.read()

    # Setup
    st.setup(
        name="notelist",
        version="0.9.2",
        description="Tag based note taking REST API",
        author="Jose A. Jimenez",
        author_email="jajimenezcarm@gmail.com",
        license="MIT",
        long_description=long_desc,
        long_description_content_type="text/markdown",
        url="https://github.com/jajimenez/notelist",
        classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
            "License :: OSI Approved :: MIT License"
        ],
        python_requires=">=3.9.0",
        install_requires=[
            "Flask==2.0.1",
            "Flask-JWT-Extended==4.3.0",
            "marshmallow==3.13.0",
            "pymongo==3.12.0",
            "boto3==1.18.59"
        ],
        packages=[
            "notelist",
            "notelist.schemas",
            "notelist.db",
            "notelist.db.base",
            "notelist.db.mongodb",
            "notelist.db.dynamodb",
            "notelist.db.localst",
            "notelist.views",
            "notelist.config"
        ],
        package_dir={
            "notelist": "src/notelist",
            "notelist.schemas": "src/notelist/schemas",
            "notelist.db": "src/notelist/db",
            "notelist.db.base": "src/notelist/db/base",
            "notelist.db.mongodb": "src/notelist/db/mongodb",
            "notelist.db.dynamodb": "src/notelist/db/dynamodb",
            "notelist.db.localst": "src/notelist/db/localst",
            "notelist.views": "src/notelist/views",
            "notelist.config": "src/notelist/config"
        },
        package_data={
            "notelist": ["templates/*.html", "static/*.css"],
            "notelist.config": ["*.json"]
        },
        entry_points={
            "console_scripts": [
                "notelist=notelist.cli:cli"
            ]
        }
    )
