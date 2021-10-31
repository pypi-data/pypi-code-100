from setuptools import setup

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="sweetrpg-client",
    install_requires=["marshmallow==3.14.0",
                      "sweetrpg-model-core",
                      "sweetrpg-api-core",
                      "sweetrpg-library-objects",
                      "requests"],
    extras_require={},
)
