from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='NlpToolkit-NER',
    version='1.0.2',
    packages=['NER', 'NER.AutoProcessor', 'NER.AutoProcessor.Sentence', 'NER.AutoProcessor.ParseTree'],
    url='https://github.com/StarlangSoftware/NER-Py',
    license='',
    author='olcaytaner',
    author_email='olcay.yildiz@ozyegin.edu.tr',
    description='NER library',
    install_requires=['NlpToolkit-AnnotatedSentence', 'NlpToolkit-AnnotatedTree'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
