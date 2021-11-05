# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tedpy']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.20.0,<0.21.0', 'xmltodict>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'tedpy',
    'version': '1.0.0',
    'description': 'Unofficial library for reading from The Energy Detective power meters',
    'long_description': '# TEDpy\n\nUnofficial library for reading from The Energy Detective power meters\n\nThis library supports the TED5000 and TED6000 devices.\n\nIt is based on [@realumhelp]\'s [ted6000py](https://github.com/realumhelp/ted6000py), Home Assistant\'s ted5000 implementation, and [@gtdiehl] and [@jesserizzo]\'s [envoy_reader](https://github.com/gtdiehl/envoy_reader/). Also huge thanks to [@realumhelp] for helping write and review much of the code!\n\n[@realumhelp]: https://github.com/realumhelp\n[@gtdiehl]: https://github.com/gtdiehl\n[@jesserizzo]: https://github.com/jesserizzo\n\n## Usage\n\n```python\nfrom tedpy import createTED\n\nHOST = \'ted6000\'\n\n# Use asyncio to deal with the async methods\ntry:\n    reader = await createTED(HOST)\n    await reader.update()\n    reader.print_to_console() # Print all information\n    print(reader.energy()) # Total energy\n    print(reader.consumption()) # Load energy only\n    print(reader.production()) # Generated energy only\n\n    print(reader.mtus[0].energy()) # Energy per MTU\n    print(reader.mtus[0].power())\n    print(reader.spyders[0].ctgroups[0].energy()) # Energy per ctgroup\n\nexcept httpx.HTTPError:\n    # Handle connection errors from createTED and update\n```\n\n## Testing\n\nTo print out your energy meter\'s values, run `poetry run python -m tedpy`.\n\nThe module\'s tests can be run using `poetry run pytest` (make sure you `poetry install` first!).\n\n## Development\n\n1. Install dependencies: `poetry install`\n2. Install pre-commit hooks: `poetry run pre-commit install`\n3. Develop!\n\n## Notes\n\n### System types\n\nThe energy meter may be configured as 1 of 3 possible `SystemType`s: `NET`, `NET_GEN`, and `LOAD_GEN` (referred to in documentation as `NET_LOAD`). `NET`, `GEN`, and `LOAD` are the possible MTU types defined as the following:\n\n- `NET`: Consumption from the grid\n- `GEN`: Solar power production\n- `LOAD`: Consumption from the grid, in the case where you are directly feeding the grid with solar\n\nIf you have not connected solar power to the meter, your system type is most likely `NET`. Otherwise, you are likely using `NET_GEN` type (measuring both grid consumption and solar power production). If you do not use an internal breaker for solar power and instead feed it directly back into the grid, you will have `LOAD_GEN` type.\n\nThe TED6000 API returns NET (net power), GEN (power generated), and LOAD (power consumed by appliances). Below is a table summarizing how these are populated for each system type. `-(x)` indicates `x` is negated. Calculated fields are italicized.\n\n| SystemType | NET                                   | GEN                             | LOAD                                      |\n|-------------|---------------------------------------|---------------------------------|-------------------------------------------|\n| `NET`       | total consumption                     | 0                               | 0                                         |\n| `NET_GEN`   | grid consumption                      | -(solar power produced)         | *grid consumption + solar power produced* |\n| `LOAD_GEN`  | *grid consumption - solar production* | -(solar power produced to grid) | grid consumption                          |\n\nWhen using the `.energy()`, `.production()`, and `.consumption()` methods, the original values of the GEN column are inverted, and `.consumption()` is populated for the `NET` type:\n\n| SystemType | `.energy()`                           | `.production()`              | `.consumption()`                          |\n|-------------|---------------------------------------|------------------------------|-------------------------------------------|\n| `NET`       | total consumption                     | 0                            | total consumption                         |\n| `NET_GEN`   | grid consumption                      | solar power produced         | *grid consumption + solar power produced* |\n| `LOAD_GEN`  | *grid consumption - solar production* | solar power produced to grid | grid consumption                          |\n\n### Inverted GEN values\n\nTo keep consistency with the `.consumption()` method, MTUs configured as `GEN` will additionally return positive `EnergyYield` values (i.e. their negative values will be inverted to positive values). It is recommended you format MTU values as such:\n\n```python\ndata = "Production" if (mtu.type == MtuType.GENERATION) else "Consumption"\nreturn f"{mtu.description} {data}: {mtu.energy()}"\n```\n\n### TED5000 consumption and production\n\nThe TED5000 API does not return a total system `.production()` and `.consumption()` value, so the library calculates one itself.\nProduction is defined as the energy sum of all MTUs marked as type "LOAD", and Consumption is defined as the energy sum of all MTUs marked as type "GEN".\n\nNET and stand-alone types of MTUs are not included in these totals, whereas they are included in the `.energy()` total of the system.\n\n### TED5000 power factor\n\nSee [#7](https://github.com/rianadon/the-energy-detective-py/issues/7) for info on how the power factor is calculated. There is a field returned by the API, but the documentation does not mention this field so the power factor is instead calculated manually.\n',
    'author': 'rianadon',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rianadon/the-energy-detective-py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
