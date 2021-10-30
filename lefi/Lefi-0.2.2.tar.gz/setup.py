# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lefi',
 'lefi.exts',
 'lefi.exts.commands',
 'lefi.exts.commands.core',
 'lefi.objects',
 'lefi.utils',
 'lefi.ws']

package_data = \
{'': ['*']}

install_requires = \
['PyNaCl>=1.4.0,<2.0.0', 'aiohttp>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'lefi',
    'version': '0.2.2',
    'description': 'A discord API wrapper focused on clean code, and usability',
    'long_description': '# Lefi\n[![Documentation Status](https://readthedocs.org/projects/lefi/badge/?version=latest)](https://lefi.readthedocs.io/en/latest/?badge=latest)\n![Pytest](https://github.com/an-dyy/Lefi/actions/workflows/run-pytest.yml/badge.svg?event=push)\n![Mypy](https://github.com/an-dyy/Lefi/actions/workflows/mypy.yml/badge.svg?event=push)\n\nA discord API wrapper focused on clean code, and usability\n\n## Installation\n\n1. Poetry\n\n   ```\n   poetry add lefi\n   ```\n\n2. Pip\n   ```\n   pip install lefi\n   ```\n\n## Example(s)\n```py\nimport os\nimport asyncio\n\nimport lefi\n\n\nasync def main() -> None:\n    token = os.getenv(\n        "discord_token"\n    )  # NOTE: I\'m on linux so I can just export, windows might need a `.env`\n    client = lefi.Client(token)  # type: ignore\n\n    @client.once("ready")\n    async def on_ready(user: lefi.User) -> None:\n        print(f"LOGGED IN AS {client_user.id}") # You can also access `client.user`\n\n    @client.on("message_create")\n    async def on_message_create(message: lefi.Message) -> None:\n        print(message)\n\n    await client.start()\n\n\nasyncio.run(main())\n```\n\n## Documentation\n[Here!](https://lefi.readthedocs.io/en/latest/)\n\n## Contributing\n1. If you plan on contributing please open an issue beforehand\n2. Fork the repo, and setup the poetry env (with dev dependencies)\n3. Install pre-commit hooks (*makes it a lot easier for me*)\n    ```\n    pre-commit install\n    ```\n\n## Contributors\n\n- [blanketsucks](https://github.com/blanketsucks) - collaborator\n- [an-dyy](https://github.com/an-dyy) - creator and maintainer\n\n',
    'author': 'an-dyy',
    'author_email': 'andy.development@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/an-dyy/Lefi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
