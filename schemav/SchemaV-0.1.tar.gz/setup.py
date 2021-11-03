from distutils.core import setup
setup(
  name = 'SchemaV',         # How you named your package folder (MyLib)
  packages = ['SchemaV'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'SchemaV validates Python dict/list structure against a schema in each step, adding default values and strcutures if needed',   # Give a short description about your library
  author = 'Abdallah Ben Hamida',                   # Type in your name
  author_email = 'noemail@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/QuanticData/SchemaV',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/QuanticData/SchemaV/archive/refs/tags/v_01.tar.gz',    # I explain this later on
  keywords = ['dict', 'python', 'schema', 'validation', 'validator', 'json', 'yml', 'yaml','specification','config','configuration'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support

  ],
)