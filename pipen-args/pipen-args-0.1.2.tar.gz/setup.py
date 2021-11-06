# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pipen_args']
install_requires = \
['diot', 'pipen', 'pyparam>=0.4.15,<0.5.0']

setup_kwargs = {
    'name': 'pipen-args',
    'version': '0.1.2',
    'description': 'Command-line argument parser for pipen.',
    'long_description': "# pipen-args\n\nCommand line argument parser for [pipen][1]\n\n## Usage\n```python\nfrom pipen import Proc, Pipen\nfrom pipen_args import args\n\nclass Process(Proc):\n    input = 'a'\n    input_data = range(10)\n    script = 'echo {{in.a}}'\n\nPipen().set_start(Process).run()\n```\n\n```\n❯ python example.py --help\n\nDESCRIPTION:\n  Pipeline description.\n  My process\n\nUSAGE:\n  example.py --in.a list [OPTIONS]\n\nOPTIONS FOR <Process>:\n  --in.a <list>                   - [Required] Undescribed.\n\nOPTIONAL OPTIONS:\n  --config <path>                 - Read options from a configuration file in TOML. Default: None\n  -h, --help                      - Print help information for this command\n  --full                          - Show full options for this command\n\nPIPELINE OPTIONS:\n  --profile <str>                 - The default profile from the configuration to run the pipeline.\n                                    This profile will be used unless a profile is specified in the\n                                    process or in the .run method of pipen. Default: default\n  --outdir <path>                 - The output directory of the pipeline\n                                    Default:\n                                    /home/pwwang/github/pipen-args/examples/pipen-0_results\n  --workdir <str>                 - The workdir for the pipeline. Default: ./.pipen\n  --scheduler <str>               - The scheduler to run the jobs. Default: local\n```\n\nSee more examples in `examples/` folder.\n\n[1]: https://github.com/pwwang/pipen\n",
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pwwang/pipen-args',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
