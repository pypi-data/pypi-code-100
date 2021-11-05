# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rhubarb', 'rhubarb.backends']

package_data = \
{'': ['*']}

install_requires = \
['aioredis>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'rhubarb-py',
    'version': '1.1.0',
    'description': 'Rhubarb is a library that simplifies realtime streaming for a number of backends into a single API',
    'long_description': '# Rhubarb\n\n<div align="center">\n\n[![Build status](https://github.com/mopeyjellyfish/rhubarb/workflows/build/badge.svg?branch=main&event=push)](https://github.com/mopeyjellyfish/rhubarb/actions?query=workflow%3Abuild)\n[![Python Version](https://img.shields.io/pypi/pyversions/rhubarb-py.svg)](https://pypi.org/project/rhubarb-py)\n[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/mopeyjellyfish/rhubarb/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)\n[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/mopeyjellyfish/rhubarb/blob/master/.pre-commit-config.yaml)\n[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/mopeyjellyfish/rhubarb/releases)\n[![License](https://img.shields.io/github/license/mopeyjellyfish/rhubarb)](https://github.com/mopeyjellyfish/rhubarb/blob/master/LICENSE)\n\nRhubarb is a library that simplifies realtime streaming of events for a number of backends in a single API\n\n</div>\n\n## Installation\n\n```bash\npip install -U rhubarb-py\n```\n\nor install with `Poetry`\n\n```bash\npoetry add rhubarb-py\n```\n\n## Example\n\nA minimal working example can be found in [example](https://github.com/mopeyjellyfish/rhubarb/blob/main/example/app.py) directory.\n\n```python\nimport os\n\nfrom starlette.applications import Starlette\nfrom starlette.concurrency import run_until_first_complete\nfrom starlette.responses import HTMLResponse\nfrom starlette.routing import Route, WebSocketRoute\n\nfrom rhubarb import Rhubarb\n\nURL = os.environ.get("URL", "redis://localhost:6379/0")\n\nevents = Rhubarb(URL)\n\nhtml = """\n<!DOCTYPE html>\n<html>\n    <head>\n        <title>Chat</title>\n    </head>\n    <body>\n        <h1>WebSocket Chat</h1>\n        <form action="" onsubmit="sendMessage(event)">\n            <input type="text" id="messageText" autocomplete="off"/>\n            <button>Send</button>\n        </form>\n        <ul id=\'messages\'>\n        </ul>\n        <script>\n            var ws = new WebSocket("ws://localhost:8000/ws");\n            ws.onmessage = function(event) {\n                var messages = document.getElementById(\'messages\')\n                var message = document.createElement(\'li\')\n                var content = document.createTextNode(event.data)\n                message.appendChild(content)\n                messages.appendChild(message)\n            };\n            function sendMessage(event) {\n                var input = document.getElementById("messageText")\n                ws.send(input.value)\n                input.value = \'\'\n                event.preventDefault()\n            }\n        </script>\n    </body>\n</html>\n"""\n\n\nasync def homepage(_):\n    return HTMLResponse(html)\n\n\nasync def room_consumer(websocket):\n    async for message in websocket.iter_text():\n        await events.publish(channel="chatroom", message=message)\n\n\nasync def room_producer(websocket):\n    async with events.subscribe(channel="chatroom") as subscriber:\n        async for event in subscriber:\n            await websocket.send_text(event.message)\n\n\nasync def ws(websocket):\n    await websocket.accept()\n    await run_until_first_complete(\n        (room_consumer, {"websocket": websocket}),\n        (room_producer, {"websocket": websocket}),\n    )\n\n\nroutes = [\n    Route("/", homepage),\n    WebSocketRoute("/ws", ws, name="chatroom_ws"),\n]\n\n\napp = Starlette(\n    routes=routes,\n    on_startup=[events.connect],\n    on_shutdown=[events.disconnect],\n)\n```\n\n\n\n## 🛡 License\n\n[![License](https://img.shields.io/github/license/mopeyjellyfish/rhubarb)](https://github.com/mopeyjellyfish/rhubarb/blob/master/LICENSE)\n\nThis project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/mopeyjellyfish/rhubarb/blob/master/LICENSE) for more details.\n\n## Credits [![🚀 Your next Python package needs a bleeding-edge project structure.](https://img.shields.io/badge/python--package--template-%F0%9F%9A%80-brightgreen)](https://github.com/TezRomacH/python-package-template)\n\nThis project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template)\n',
    'author': 'mopeyjellyfish',
    'author_email': 'dev@davidhall.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mopeyjellyfish/rhubarb',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
