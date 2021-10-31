from setuptools import setup, find_packages

VERSION = '0.0.5'
DESCRIPTION = 'This is whatsapp group chat analysis package which will basically help you to extract amazing insights from the group chat and create beautiful interactive visuals' \
              ' in just 2 to 3 lines of code. You do not have to worry about anything, just load the chat file, create an object and use it.'
LONG_DESCRIPTION = \
    'This is whatsapp group chat analysis package which will basically extract the insights from the whatsapp group chat and create beautiful interactive visuals in just 2 to 3 lines of code. ' \
    'You do not have to worry about anything, just load the chat file, create an object, and use it. There are more than 15 methods are available which will help you ' \
    'to create beautiful user-interactive charts. Even you can download the preprocessed data, charts, and use it for further analysis. This is my small open source contribution to python\'s community.'\
    ' For more details visit : https://github.com/ronylpatil/whatsapplib'

# Setting up
setup(
    name="WhatsappLib",
    packages=find_packages(),
    version=VERSION,
    license='MIT',
    author="ronil08",
    url = 'https://github.com/ronylpatil/whatsapplib',
    author_email="ronyy0080@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    install_requires=['plotly', 'nltk', 'numpy', 'emoji', 'wordcloud', 'matplotlib', 'pandas'],
    keywords=['whatsapp analyzer', 'whatsapp lib', 'whatsapp analysis', 'whatsapp python', 'chat', 'whatsapp group chat analysis', 'whatsapp library', 'ronil patil', 'ronil08', 'website', 'download', 'links', 'images', 'videos'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',
        "Intended Audience :: Developers",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)