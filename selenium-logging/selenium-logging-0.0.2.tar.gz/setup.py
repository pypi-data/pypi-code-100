import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="selenium-logging",
    version="0.0.2",
    author="smirad91",
    author_email="smirad91@gmail.com",
    description="Log messages and images in HTML file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/smirad91/LoggingSelenium",
    project_urls={
        "Bug Tracker": "https://github.com/smirad91/LoggingSelenium/issues",
    },
    install_requires=["pyautogui", "datetime"],
    keywords=["log", "selenium", "automation", "screenshot", "message", "HTML"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    packages=setuptools.find_packages()
)