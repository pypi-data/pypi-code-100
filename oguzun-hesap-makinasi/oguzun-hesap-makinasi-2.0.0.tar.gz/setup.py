import pathlib
from setuptools import setup,setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

print(HERE)

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="oguzun-hesap-makinasi",
    version="2.0.0",
    description="muratin hesap makinasi",
    long_description=README,    # check işlemnde ozellikle hata almak için açıklama satırına çevrildi.
    long_description_content_type="text/markdown",
    url="https://github.com/muratcabuk/muratin-hesap-makinasi",
    author="murat cabuk",
    author_email="mcabuk@gmail.com",
    license="MIT",
    classifiers=[
            'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3.7",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src",exclude=("tests",)),
    include_package_data=True,
    install_requires=["requests >= 2.0.0", "click >= 8.0.0"],
    python_requires=">=3.0",
    options={"bdist_wheel": {"universal": "1"}},
    entry_points={
        "console_scripts": [
            "muratin_hesap_makinasi=muratin_hesap_makinasi.__main__:main", 
            # kurulum yapıldıktan sonra doğrudan uygulama gibi çağrılacaksa eşittirin solunda ne yazıyorsa o kelime konsole daçağrılır
        ]
    },
)