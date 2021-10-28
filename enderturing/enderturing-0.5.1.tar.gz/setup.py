# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['enderturing',
 'enderturing.api',
 'enderturing.api.schemas',
 'enderturing.config']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.1,<2.0.0', 'requests>=2.25.1,<3.0.0', 'websockets>=8.1,<9.0']

setup_kwargs = {
    'name': 'enderturing',
    'version': '0.5.1',
    'description': 'Python SDK for EnderTuring speech toolkit',
    'long_description': '# Ender Turing\n\nEnder Turing is a solution for voice content understanding, analytics and business insights.\nCheck [enderturing.com](https://enderturing.com/) for details.\n\n## Installation\n\n```shell\n$ pip install enderturing\n```\n\nFor using streaming speech recognition functions, you\'ll also need FFmpeg installed.\n\nUbuntu:\n```shell\n$ sudo apt install ffmpeg\n```\n\nMacOS homebrew:\n```shell\n$ brew install ffmpeg\n```\n\nFor other OS, please follow FFmpeg installation guides.\n\n## Quick Start\n\n```python\nimport asyncio\nfrom enderturing import Config, EnderTuring, RecognitionResultFormat\n\n# create configuration\nconfig = Config.from_url("https://admin%40local.enderturing.com:your_password@enterturing.yourcompany.com")\net = EnderTuring(config)\n\n# access sessions list\nsessions = et.sessions.list()\nprint(sessions)\n\n# get recognizer for one of configured languages\nrecognizer = et.get_speech_recognizer(language=\'en\')\n\nasync def run_stream_recog(f, r, result_format):\n    async with r.stream_recognize(f, result_format=result_format) as rec:\n        text = await rec.read()\n    return text\n\n# recognize specified file\nloop = asyncio.get_event_loop()\ntask = loop.create_task(run_stream_recog("my_audio.mp3", recognizer, result_format=RecognitionResultFormat.text))\nloop.run_until_complete(task)\nprint(task.result())\n```\n\n## Usage\n\nSDK contains two major parts:\n\n- Using Ender Turing REST API\n- Speech recognition\n\n## Using Ender Turing API\n\nAll API calls are accessible via an instance or `EnderTuring`. API methods are grouped, and each\ngroup is a property of `EnderTuring`. Examples:\n```python\nfrom enderturing import Config, EnderTuring, RecognitionResultFormat\n\net = EnderTuring(Config.from_env())\n\n# access sessions list\nsessions = et.sessions.list()\n\n# working with ASR\net.asr.get_instances(active_only=True)\n\n# accessing raw json\net.raw.create_event(caller_id=\'1234\', event_data={"type": "hold"})\n```\n\n## Access Configuration\n\nTo access API, you need to know an authentication key (login), authentication secret (password), and\ninstallation URL (e.g. https://enderturing.yourcompany.com/)\n\nThere are multiple ways to pass config options:\n\n- from environmental variables (`Config.from_env()`).\n- creating `Config` with parameters (e.g. `Config(auth_key="my_login", auth_secret="my_secret"")`)\n- using Enter Turing configuration URL (`Config.from_url()`)\n\n## Creating Speech Recognizer\n\nThere two options to create a speech recognizer:\n\n### If you have access to API configured:\n```python\nrecognizer = et.get_speech_recognizer(language=\'en\')\n```\n\n### If you know URL and sample rate of desired ASR instance:\n```python\nfrom enderturing import AsrConfig, SpeechRecognizer\n\nconfig = AsrConfig(url="wss://enderturing", sample_rate=8000)\nrecognizer = SpeechRecognizer(config)\n```\n\n## Recognizing a File\n\n`SpeechRecognizer.recognize_file` method returns an async text stream. Depending on parameters,\neach line contains either a text of utterance or serialized JSON.\n\nIf you are only interested in results after recognition is complete, you can use the `read()` method. E.g.\n\n```python\nasync with recognizer.recognize_file("my_audio.wav", result_format=RecognitionResultFormat.text) as rec:\n    text = await rec.read()\n```\n\nIf you prefer getting words and phrases as soon as they are recognized - you can\nuse the `readline()` method instead. E.g.\n\n```python\nasync with recognizer.recognize_file(src, result_format=RecognitionResultFormat.jsonl) as rec:\n    line = await rec.readline()\n    while line:\n        # Now line contains a json string, you can save it or do something else with it\n        line = await rec.readline()\n\n```\n\n## Working With Multichannel Audio\n\nIf an audio file has more than one channel - by default system will recognize each channel and\nreturn a transcript for each channel. To change the default behavior - you can use `channels`\nparameter of `SpeechRecognizer.recognize_file`. Please check method documentation for details.\n\nSometimes an audio is stored as a file per channel, e.g., contact center call generates two files:\none for a client and one for a support agent. But for analysis, it\'s preferable to see transcripts\nof the files merged as a dialog. In this scenario, you can use\n`recognizer.recognize_joined_file([audio1, audio2])`.\n\n## License\n\nReleased under the MIT license.\n',
    'author': 'EnderTuring',
    'author_email': 'info@enderturing.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://enderturing.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
