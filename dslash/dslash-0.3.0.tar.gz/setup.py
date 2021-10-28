# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dslash']

package_data = \
{'': ['*']}

install_requires = \
['nextcord>=2.0.0-alpha.3,<3.0.0']

setup_kwargs = {
    'name': 'dslash',
    'version': '0.3.0',
    'description': 'A library which supplements Nextcord by adding support for slash commands.',
    'long_description': '# DSlash\n\n![Version: 0.3.0](https://img.shields.io/badge/Version-0.3.0-red?style=flat-square)\n[![Code Style: black](https://img.shields.io/badge/Code%20Style-black-black?style=flat-square)](https://github.com/psf/black)\n[![License: MIT](https://img.shields.io/badge/License-MIT-orange?style=flat-square)](./LICENSE)\n[![PyPI: dslash](https://img.shields.io/badge/PyPI-dslash-green?style=flat-square)](https://pypi.org/project/dslash)\n![Python: ^3.9](https://img.shields.io/badge/python-%5E3.9-blue?style=flat-square)\n\nA library which supplements [Nextcord](https://github.com/nextcord/nextcord)\n(a fork of Discord.py) by adding support for slash commands.\n\nDocumentation is still a work in progress, and the library should currently be\nconsidered unstable.\n\nYou can install it using pip, eg. `pip install dslash`.\n\n## Example\n\n```python\nimport random\nimport logging\nimport traceback\n\nfrom nextcord import Embed, Interaction, Member, Role\nfrom dslash import Choices, CommandClient, SlashCommandInvokeError, allow_roles, option\n\n\nGUILD_ID = ...\nADMIN_ROLE_ID = ...\nTOKEN = ...\n\nlogging.basicConfig(level=logging.INFO)\nclient = CommandClient(guild_id=GUILD_ID)\n\n\n@client.event\nasync def on_ready():\n    print(f\'Logged in as {client.user}.\')\n\n\n@client.command()\nasync def roll(\n        interaction: Interaction,\n        sides: int = option(\'How many sides (default 6).\')):\n    """Roll a dice."""\n    value = random.randint(1, sides or 6)\n    await interaction.response.send_message(f\'You got: {value}\')\n\n\nimages = client.group(\'images\', \'Cute image commands.\')\n\n\n@images.subcommand()\nasync def cat(interaction: Interaction):\n    """Get a cat image."""\n    await interaction.response.send_message(\n        embed=Embed().set_image(url=\'https://cataas.com/cat\')\n    )\n\n\n@images.subcommand()\nasync def dog(interaction: Interaction):\n    """Get a dog image."""\n    await interaction.response.send_message(\n        embed=Embed().set_image(url=\'https://placedog.net/500?random\')\n    )\n\n\n@images.subcommand(name=\'any\')\nasync def any_(interaction: Interaction):\n    """Get any random image."""\n    await interaction.response.send_message(\n        embed=Embed().set_image(url=\'https://picsum.photos/600\')\n    )\n\n\nadmin = client.group(\n    \'admin\',\n    \'Admin-only commands.\',\n    default_permission=False,\n    permissions=allow_roles(ADMIN_ROLE_ID)\n)\nroles = admin.subgroup(\'roles\', \'Commands to manage roles.\')\n\n\n@roles.subcommand(name=\'del\')\nasync def del_(\n        interaction: Interaction, role: Role = option(\'The role to delete.\')):\n    """Delete a role."""\n    await role.delete()\n    await interaction.response.send_message(\'Deleted the role.\', ephemeral=True)\n\n\n@allow_roles(ADMIN_ROLE_ID)\n@client.command(default_permission=False)\nasync def ban(\n        interaction: Interaction, user: Member = option(\'The user to ban.\')):\n    """Ban a user."""\n    await user.ban()\n    await interaction.response.send_message(\'Banned the user.\', ephemeral=True)\n\n\nclass RPSChoices(Choices):\n    rock = \'Rock\'\n    paper = \'Paper\'\n    scissors = \'Scissors\'\n    gun = \'Gun\'\n\n\n@client.command()\nasync def rps(interaction: Interaction, choice: RPSChoices = option(\'Your choice.\')):\n    """Play rock, paper, scissors."""\n    if choice == RPSChoices.gun:\n        await interaction.response.send_message("That\'s cheating!")\n    else:\n        await interaction.response.send_message(f\'You picked {choice.name}.\')\n\n\nclient.run(TOKEN)\n```\n\n## Planned Features\n\n- Using `Optional[...]` for optional arguments.\n- Using docstring conventions for option descriptions.\n- Removing the `option()` default-as-decorator.\n- Class-based command groups, like `nextcord.ext.commands` cogs.\n\nCompatibility with `nextcord.ext.commands` is not planned.\n\n## Development\n\nAs well as Python 3.9+, this project requires Poetry for development.\n[Click this link for installation instructions](https://python-poetry.org/docs/master/#installation),\nor:\n\n- #### \\*nix (Linux/MacOS)\n\n  `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -`\n\n- #### Windows Powershell\n\n  `(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -UseBasicParsing).Content | python -`\n\nOnce you have Poetry installed:\n\n1. **Create a virtual environment:** `poetry shell`\n2. **Install dependencies:** `poetry install`\n\nThe following commands are then available:\n\n- `poe format` - Run auto-formatting and linting.\n\nPrefix these with `poetry run` if outside of the Poetry shell.\n',
    'author': 'Artemis',
    'author_email': 'me@arty.li',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/artemis21/dslash',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
