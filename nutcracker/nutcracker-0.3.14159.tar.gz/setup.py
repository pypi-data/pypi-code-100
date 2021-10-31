# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nutcracker',
 'nutcracker.chiper',
 'nutcracker.codex',
 'nutcracker.earwax',
 'nutcracker.graphics',
 'nutcracker.kernel',
 'nutcracker.smush',
 'nutcracker.sputm',
 'nutcracker.sputm.char',
 'nutcracker.sputm.costume',
 'nutcracker.sputm.room',
 'nutcracker.sputm.script',
 'nutcracker.sputm_old',
 'nutcracker.utils']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.0.1,<9.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'deal>=4.5.0,<5.0.0',
 'numpy>=1.19.1,<2.0.0',
 'parse>=1.18.0,<2.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['nutcracker = nutcracker.runner:app',
                     'smush = nutcracker.smush.runner:app']}

setup_kwargs = {
    'name': 'nutcracker',
    'version': '0.3.14159',
    'description': 'Tools for editing resources in SCUMM games.',
    'long_description': "# NUTCracker\nTools for editing resources in SCUMM games.\n\n## Features:\n* Extract and Edit fonts for v5-v7 + HE\n* Extract and Edit NUT fonts - v7-v8\n* Extract and Replace SMUSH video frames\n* Compress SMUSH videos (like scummvm-tools)\n* Extract and Rebuild game resources - v5-v8 + HE\n* Extract and Inject text strings - v5-v8 + HE\n* Extract and Replace background and objects images - v5-v8 + HE (option to extract EGA backgrounds)\n* Decompile V5 Scripts to Windex-like (SCUMM debugger from https://quickandeasysoftware.net/monkey-island-2-talkie-prototype) syntax\n\n## Resources\n\n### Extract and rebuild\n\nSupported games: V5-V8, HE\n\nExtract game resources to patch files using:\n```\nnutcracker sputm extract PATH/TO/GAME.000\n```\n*Replace `PATH/TO/GAME.000` to actual game index file (Usually ends with `.000`, `.LA0` or `.HE0`)\n\nThis also creates XML-like file `rpdump.xml` to show which files were extracted.\n\nRebuild game resources from patches (using original resource as reference):\n```\nnutcracker sputm build --ref PATH/TO/GAME.000 GAME\n```\n\n## Fonts\n\n### SPUTM Font (`CHAR` chunks)\n\nSupported games: V5-V7, HE\n\nExtract the fonts using:\n```\nnutcracker sputm fonts_extract PATH/TO/GAME.000\n```\n\n*Replace `PATH/TO/GAME.000` to actual game index file (Usually ends with `.000`, `.LA0` or `.HE0`)\n\nfonts will be extracted as PNG images to directory `GAME/chars` relative to workdir.\n\n*Replace `GAME` with name of the game (e.g. `ATLANTIS` if game index file is `ATLANTIS.000`)\n\nModify the font images with any image editor.\n\nCreate patch files for the modified font:\n```\nnutcracker sputm fonts_inject --ref PATH/TO/GAME.000 GAME\n```\nRebuild game resources\n```\nnutcracker sputm build --ref PATH/TO/GAME.000 GAME\n```\n\n### NUT Fonts\n\nSupported games: V7-V8\n\n#### Decoding\nDecode all NUT files in given directory DATADIR\n```\nnutcracker smush decode DATADIR/*.NUT --nut --target OUTDIR\n```\nCreates a font image file named chars.png in OUTDIR which can be edited using regular image editing software (e.g. GIMP)\n\n#### Encoding\nEncode given font image (PNG_FILE) with given codec number (CODEC) using REF_NUT_FILE as reference\n```\npython -m nutcracker.smush.encode PNG_FILE --target NEW_NUT_FILE --ref REF_NUT_FILE --codec CODEC [--fake CODEC]\n```\nThis will convert font image file back to font file (NEW_NUT_FILE) which can be used in game.\n\nAvailable codecs: \n* 21 (FT + The Dig*)\n* 44 (COMI*)\n\n*FONT3.NUT and the fonts in The Dig was actually encoded using codec 21 method but marked as 44.\nIt can be achieved using `--codec 21 --fake 44`.\nsee examples in [test.bat](test.bat)\n\n## SMUSH Videos\n\n### Decode and Re-encode\n\nSupported games: V7-V8\n\nDecode frames using\n```\nnutcracker smush decode DATADIR/*.SAN --target OUTDIR\n```\nFrames will be extracted as PNG files to `OUTDIR/VIDEO.SAN`\nwhere `VIDEO.SAN` matches the filename of the video.\n\nRe-encode the video using:\n```\npython -m nutcracker.smush.encode_san_seq DATADIR/VIDEO.SAN\n``` \nwhere DATADIR/VIDEO.SAN is path to original SMUSH video file\n\nThe new video will be created as `NEW_VIDEO2.SAN` in workdir\n\n*To reduce result file size, it is recommended to only re-encode modified frames, this can be done by removing unaltered frames from `OUTDIR/VIDEO.SAN`\n\n### Compress\n\nSupported games: V7-V8\n\nCompress video frames using zlib compression, as in scummvm-tools\n```\nnutcracker smush compress DATADIR/*.SAN\n```\n\n## Text\n\n### Extract and Inject script text\n\nSupported games: V5-V8, HE\n\nExtract all texts from game to text file using:\n```\nnutcracker sputm strings_extract --textfile strings.txt PATH/TO/GAME.000\n```\n*Replace `PATH/TO/GAME.000` to actual game index file (Usually ends with `.000`, `.LA0` or `.HE0`)\n\nEdit the text file using regular text editor.\n\nInject the modified text in game resources using:\n```\nnutcracker sputm strings_inject  --textfile strings.txt PATH/TO/GAME.000\n```\n\n### Decompile game script\n\nSupported games: V5\n\nDecompile game scripts to script file with Windex-like syntax:\n\n```\npython -m nutcracker.sputm.windex_v5 PATH/TO/GAME.000\n```\n*Replace `PATH/TO/GAME.000` to actual game index file (Usually ends with `.000`, `.LA0` or `.HE0`)\n\n\n## Graphics\n\n### Room background and object images\n\nSupported games: V5-V8, HE\n\nExtract room background and object images using:\n\n```\nnutcracker sputm room decode [--ega] PATH/TO/GAME.000\n```\n*Replace `PATH/TO/GAME.000` to actual game index file (Usually ends with `.000`, `.LA0` or `.HE0`)\n\n*Use the `--ega` if you wish to simulate EGA graphics on games with EGA backward compatibility mode, don't use it if you wish to modify the graphics for injecting modified graphics later\n\nRoom backgrounds and Object images will be extracted as PNG images in `GAME/backgrounds` and `GAME/objects` respectively, where `GAME` is replaced with the name of the game.\n\nModify the image files, it's recommended to use image editor without palette optimization, such as GraphicsGale.\n\nCreate patch files for the modified images using:\n```\nnutcracker sputm room encode --ref PATH/TO/GAME.000 GAME\n```\nRebuild game resources\n```\nnutcracker sputm build --ref PATH/TO/GAME.000 GAME\n```\n",
    'author': 'BLooperZ',
    'author_email': 'blooperz@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
