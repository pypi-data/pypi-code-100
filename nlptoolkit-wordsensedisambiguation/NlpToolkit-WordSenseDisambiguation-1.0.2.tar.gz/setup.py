from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='NlpToolkit-WordSenseDisambiguation',
    version='1.0.2',
    packages=['WordSenseDisambiguation', 'WordSenseDisambiguation.Sentence', 'WordSenseDisambiguation.ParseTree'],
    url='https://github.com/StarlangSoftware/WordSenseDisambiguation-Py',
    license='',
    author='olcaytaner',
    author_email='olcay.yildiz@ozyegin.edu.tr',
    description='Word Sense Disambiguation Library',
    install_requires = ['NlpToolkit-AnnotatedSentence', 'NlpToolkit-AnnotatedTree'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
