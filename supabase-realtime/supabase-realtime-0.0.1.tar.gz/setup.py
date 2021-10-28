# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['realtime']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8.1,<3.0.0', 'websockets>=9.1,<10.0']

setup_kwargs = {
    'name': 'supabase-realtime',
    'version': '0.0.1',
    'description': 'Listen to changes on your supabase postgres database.',
    'long_description': '# supabase-realtime-client\n\nPython Client Library to interface with the Phoenix Realtime Server\nThis is a fork of the [supabase community realtime client library](https://github.com/supabase-community/realtime-py).\nI am maintaining this fork, to use it under the hood in another project.\n\n## Quick Start\n\n```python\nimport asyncio\nfrom realtime import Socket\n\ndef callback1(payload):\n    print("Callback 1: ", payload)\n\ndef callback2(payload):\n    print("Callback 2: ", payload)\n\nasync def main() -> None:\n    URL = "ws://localhost:4000/socket/websocket"\n    s = Socket(URL)\n    await s.connect()\n\n    # join channels\n    channel_1 = s.set_channel("realtime:public:todos")\n    await channel_1.join()\n    channel_2 = s.set_channel("realtime:public:users")\n    await channel_2.join()\n\n    # register callbacks\n    channel_1.on("UPDATE", callback1)\n    channel_2.on("*", callback2)\n\n    s.listen()  # infinite loop\n```\n\n## Sample usage with Supabase\n\nHere\'s how you could connect to your realtime endpoint using Supabase endpoint. Please replace `SUPABASE_ID` and `API_KEY` with your own `SUPABASE_ID` and `API_KEY`. The variables shown below are fake and they will not work if you try to run the snippet.\n\n```python\nimport asyncio\nfrom realtime import Socket\n\nSUPABASE_ID = "dlzlllxhaakqdmaapvji"\nAPI_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYW5vbiIsImlhdCI6MT"\n\n\ndef callback1(payload):\n    print("Callback 1: ", payload)\n\nasync def main() -> None:\n    URL = f"wss://{SUPABASE_ID}.supabase.co/realtime/v1/websocket?apikey={API_KEY}&vsn=1.0.0"\n    s = Socket(URL)\n    await s.connect()\n\n    channel_1 = s.set_channel("realtime:*")\n    await channel_1.join()\n    channel_1.on("UPDATE", callback1)\n\n    s.listen()\n```\n\nThen, go to the Supabase interface and toggle a row in a table. You should see a corresponding payload show up in your console/terminal.\n',
    'author': 'Anand Krishna',
    'author_email': 'anandkrishna2312@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/anand2312/supabase-realtime-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
