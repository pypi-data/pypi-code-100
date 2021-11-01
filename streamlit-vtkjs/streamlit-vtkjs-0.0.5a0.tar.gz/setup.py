import setuptools

setuptools.setup(
    name="streamlit-vtkjs",
    version="0.0.5-alpha",
    author="Pollination",
    author_email="nicolas@ladybug.tools",
    description="vtkjs component for streamlit",
    long_description="vtkjs component for streamlit",
    long_description_content_type="text/plain",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 0.63",
    ],
)
