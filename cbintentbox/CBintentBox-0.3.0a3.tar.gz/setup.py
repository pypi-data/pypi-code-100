from setuptools import setup

setup(
    name='CBintentBox',
    version='0.3.0a3',
    packages=['intentBox',
              'intentBox.coreference',
              'intentBox.intent_assistant',
              'intentBox.lang',
              'intentBox.parsers',
              'intentBox.segmentation',
              'intentBox.utils'
              ],
    url='https://github.com/HelloChatterbox/intentBox',
    license='',
    author='hellochatterbox',
    install_requires=["adapt-parser>=0.3.3", "padacioso", "auto_regex",
                      "quebra_frases>=0.3.1", "nebulento>=0.1.0"],
    author_email='jarbasai@mailfence.com',
    extras_require={
        "extras": ["requests", "padaos>=0.1.9", "padatious>=0.4.6",
                   "palavreado>=0.2.0", "fann2>=1.0.7", "pronomial>=0.0.8",
                   "RAKEkeywords"]
    },
    description='chatterbox intent parser, extract multiple intents from a single utterance '
)
