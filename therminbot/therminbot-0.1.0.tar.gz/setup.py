from distutils.core import setup


setup(
    name="therminbot",
    packages=["therminbot"],
    version="0.1.0",
    license="MIT",
    description="Multifunctional human-friendly 20% sarcastic bot.",
    author = "Alexander Ryzhov",
    author_email = "thed4rkof@gmail.com",
    url = "https://github.com/ryzhovalex/therminbot",
    download_url = "",
    keywords = ["telegram-bot", "service-bot", "multi-bot"],
    install_requires=[
        "aiogram",
        "warepy",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
    ],
)