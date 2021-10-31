# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['turdshovel',
 'turdshovel._stubs.Microsoft',
 'turdshovel._stubs.Microsoft.Diagnostics',
 'turdshovel._stubs.Microsoft.Diagnostics.NETCore',
 'turdshovel._stubs.Microsoft.Diagnostics.Runtime',
 'turdshovel._stubs.Microsoft.Diagnostics.Runtime.DataReaders',
 'turdshovel._stubs.System',
 'turdshovel._stubs.System.Buffers',
 'turdshovel._stubs.System.Collections',
 'turdshovel._stubs.System.Reflection',
 'turdshovel._stubs.System.Reflection.Metadata',
 'turdshovel._stubs.System.Runtime',
 'turdshovel._stubs.System.Threading',
 'turdshovel._stubs.System.Threading.Tasks',
 'turdshovel.commands',
 'turdshovel.core']

package_data = \
{'': ['*'], 'turdshovel': ['_dlls/*']}

install_requires = \
['numpy>=1.21.2,<2.0.0',
 'orjson>=3.6.4,<4.0.0',
 'pyparsing==2.4.7',
 'python-nubia>=0.2b5,<0.3',
 'pythonnet>=2.5.2,<3.0.0',
 'rich>=10.12.0,<11.0.0']

entry_points = \
{'console_scripts': ['turdshovel = turdshovel.main:init']}

setup_kwargs = {
    'name': 'turdshovel',
    'version': '0.2.1',
    'description': 'Looks through memory dumps for secrets',
    'long_description': '# Turdshovel\n\n\n<p align=\'center\'><img src=\'https://github.com/daddycocoaman/turdshovel/raw/main/docs/images/logo.png\' alt=\'logo\' height="400"/></p>\n\n# Description\n\nTurdshovel is an interactive CLI tool that allows users to dump objects from .NET memory dumps without having to fully understand the intricacies of WinDbg. It uses [Python.NET](https://github.com/pythonnet/pythonnet) to wrap around [ClrMD](https://github.com/microsoft/clrmd) and perform basic operations for dumping objects and sections of memory. The primary goal of Turdshovel is to focus on finding secrets in memory dumps quickly.\n\n**It is absolutely not intended to be a full-fledged memory dump analysis tool.**\n\n# Installation\n\nTurdshovel is written in Python 3.8 and at the moment is expected to only work with Python 3.8. No testing has been performed with other Python versions. This is because Turdshovel has a dependency on [Python.NET](https://github.com/pythonnet/pythonnet), which requires specific installations of its files per Python version. This may change in the future with the release of Python.NET 3.0 and Turdshovel will support Python >3.8 as long as Python.NET supports it.\n\nAdditionally, Turdshovel is meant to be installed on **Windows** and has only been tested on **Windows**. No testing has been performed with Linux. However, Turdshovel uses the .NET Standard 2.0 versions of [ClrMD](https://github.com/microsoft/clrmd) which supports:\n\n- .NET Core (2.0 - 6.0)\n- .NET Framework (4.6.1 - 4.8)\n- Mono (5.4, 6.4)\n\nThe inclusion of Mono may mean that Turdshovel works on Linux, especially since [ClrMD does support Linux](https://github.com/microsoft/clrmd/blob/master/doc/FAQ.md#what-platforms-are-supported). However, future plans for Turdshovel may include features that will be limited to Windows due to dependencies. These features will not be supported on other OSes, so a Windows environment is your best bet for usage.\n\nMicrosoft offers free Windows 10 development environment VMs [here](https://developer.microsoft.com/en-us/windows/downloads/virtual-machines/).\n\n## Installing with Pipx\n\nAs a CLI tool, installation is highly recommended using [Pipx](https://github.com/pypa/pipx) to avoid any dependency confusions. **Honestly, you should use Pipx for most Python CLI tools!** Additionally, since Turdshovel only works with Python 3.8, this helps ensure that your virtual environment is set to use Python 3.8 at all times.\n\nIf your Pipx install was done with Python 3.8:  ```pipx install turdshovel```\n\nIf your Pipx install was done with different version: ```pipx install --python <path/to/python3.8> turdshovel```\n<br>\n<br>\n# Usage\n\nTurdshovel uses [Nubia](https://github.com/facebookincubator/python-nubia) as its framework for an interactive CLI.\n\n| Command   | Arguments                                                                       | Description                           |\n| :-------- | :------------------------------------------------------------------------------ | :------------------------------------ |\n| load      |                                                                                 | Loads a dump for a session            |\n| dump heap | **filter** - Filter objects by strings                                          | Lists objects on the heap             |\n| dump obj  | **address** - Address of object to dump<br>**save** - Save ouput to disk        | Dumps object on heap by address       |\n| dump mem  | **address** - Address of memory to read<br>**length** - Length of bytes to read | Dumps the memory in bytes at location |\n| help      |                                                                                 | Show help                             |\n| exit      |                                                                                 | Exit                                  |\n\n---\n##  Commands\n\n<details>\n<summary>load</summary>\n\nThe `load` command takes the path to the file dump as an argument.\n\n<p align=\'center\'><img src=\'https://github.com/daddycocoaman/turdshovel/raw/main/docs/images/loadcommand.png\' alt=\'load command\' height="700"/></p>\n\n\n</details>\n\n<details>\n<summary>dump heap</summary>\n\nSimilar to the dump heap command via [SOS](https://docs.microsoft.com/en-us/dotnet/core/diagnostics/sos-debugging-extension), this command will list the objects on the heap as well as their type. However, the output differs in that Turdshovel does not show objects which are listed as "Free" on the heap. You can optionally pass a list of strings as the filter.\n\n<p align=\'center\'><img src=\'https://github.com/daddycocoaman/turdshovel/raw/main/docs/images/dumpheap.png\' alt=\'dump heap\' height="400"/></p>\n</details>\n\n<details>\n<summary>dump obj</summary>\n\nSimilar to the dump obj command via [SOS](https://docs.microsoft.com/en-us/dotnet/core/diagnostics/sos-debugging-extension), this command will dump all of the non-static fields of the object on the heap in JSON representation. You can also pass `save=True` to save the resulting JSON to disk.\n<br><br>\n\n**IMPORTANT:** When dumping a complex object, you may noticed fields `<!>`. This indicates that the field would have caused a recursion error to occur so Turdshovel did not parse the field. This usually occurs with objects that reference themselves.\n\n<p align=\'center\'><img src=\'https://github.com/daddycocoaman/turdshovel/raw/main/docs/images/dumpobj1.png\' alt=\'dump obj 1\' width="1100"/></p>\n<p align=\'center\'><img src=\'https://github.com/daddycocoaman/turdshovel/raw/main/docs/images/dumpobj2.png\' alt=\'dump obj 2\' width="1100"/></p>\n\n</details>\n\n<details>\n<summary>dump mem</summary>\nPrints the bytes at the location specified for the amount of bytes specified. This is useful when objects point to locations in memory that are not objects, such as encrypted data, or just seeing what is around any given memory address. The example shows a simple string which you could find with the strings command but there are better use cases, specifically with pointers!\n\n<p align=\'center\'><img src=\'https://github.com/daddycocoaman/turdshovel/raw/main/docs/images/loadcommand.png\' alt=\'dump mem\'/></p>\n\n\n</details>\n<br>\n\n# Built With\n- [Python-Nubia](https://github.com/facebookincubator/python-nubia) - CLI Framework\n- [Python.NET](https://github.com/pythonnet/pythonnet) - Python/C# Interop\n- [ClrMD](https://github.com/microsoft/clrmd) - .NET Diagnostics Library\n- [Rich](https://github.com/willmcgugan/rich) - Amazing text, highlighting, and formatting\n<br>\n\n# Special Thanks\n- [Steve Dower](https://twitter.com/zooba) - Helped fixed the recursion issue!',
    'author': 'Leron Gray',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/daddycocoaman/turdshovel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<3.9',
}


setup(**setup_kwargs)
