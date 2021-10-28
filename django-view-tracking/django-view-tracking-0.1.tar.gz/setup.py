import pathlib
from setuptools import setup

README = (pathlib.Path(__file__).parent / "README.md").read_text()

setup(
    name="django-view-tracking",
    version="0.1",
    description="Simple logging of user access to URLs in Django.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/accu-trade/django-view-tracking",
    author="Accu-Trade LLC",
    license="MIT",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    packages=["django_view_tracking", "django_view_tracking.migrations"],
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=["Django>=2.2"],
)
