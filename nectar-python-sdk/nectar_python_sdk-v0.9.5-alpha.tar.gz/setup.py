from distutils.core import setup
setup(
  name = 'nectar_python_sdk',         # How you named your package folder (MyLib)
  packages = ['nectar_python_sdk'],   # Chose the same as "name"
  version = 'v0.9.5-alpha',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Nectar API helper SDK. Generate STS compliant prepaid tokens',   # Give a short description about your library
  author = 'Reagan Mbitiru',                   # Type in your name
  author_email = 'reagan@nectar.software',      # Type in your E-Mail
  url = 'https://github.com/Reagan/nectar-python-sdk',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Reagan/nectar-python-sdk/archive/refs/tags/v0.9.4-alpha.tar.gz',    # I explain this later on
  keywords = ['sts', 'prepaid', 'tokens', 'nectar api'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'requests',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6',
  ],
)
