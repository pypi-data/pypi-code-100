# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pelican', 'pelican.plugins.avatar']

package_data = \
{'': ['*']}

install_requires = \
['libgravatar>=0.2.5', 'pelican>=4.5', 'py3dns>=3.2', 'pylibravatar>=1.7']

extras_require = \
{'markdown': ['markdown>=3.2']}

setup_kwargs = {
    'name': 'pelican-avatar',
    'version': '1.0.1',
    'description': 'Libravatar/Gravatar plugin for Pelican',
    'long_description': 'Avatar: A Plugin for Pelican\n============================\n\n[![Build Status](https://img.shields.io/github/workflow/status/pelican-plugins/avatar/build)](https://github.com/pelican-plugins/avatar/actions)\n[![PyPI Version](https://img.shields.io/pypi/v/pelican-avatar)](https://pypi.org/project/pelican-avatar/)\n![License](https://img.shields.io/pypi/l/pelican-avatar?color=blue)\n\nThis plugin allows the inclusion of [Libravatar][] or [Gravatar][] user profile pictures, corresponding to the email address of the article\'s author.\n\n[Libravatar]: http://www.libravatar.org\n[Gravatar]: http://www.gravatar.com\n\nInstallation\n------------\n\nThis plugin can be installed via:\n\n    python -m pip install pelican-avatar\n\nUsage\n-----\n\n### Specifying the Author\'s Email Address\n\nThe default email address is taken from the `AVATAR_AUTHOR_EMAIL` variable in the Pelican settings file. This default value can be overridden on a per-article basis by specifying an email address in the article\'s metadata:\n\nFor reStructuredText:\n\n```rst\n:email: bart.simpson@example.com\n```\n\nFor Markdown:\n\n```markdown\nEmail: bart.simpson@example.com\n```\n\nThe plugin first tries to find an avatar image corresponding to the specified email at Libravatar. If it is not found there, the plugin then searches Gravatar. If an avatar for the specified email address is not found at any of those services, a default picture is shown. The default for the "missing picture" can be defined in the configuration variable `AVATAR_MISSING`.\n\n### Adjusting the Template\n\nThis plugin assigns the `author_avatar` variable to the avatar image URL and makes that variable available within the article\'s context. For instance, you can add the following to a template file (for example, to the `article_infos.html` template file), just before the information about the author:\n\n```html\n{% if article.author_avatar %}\n<div align="center">\n        <img src="{{ article.author_avatar }}">\n</div>\n{% endif %}\n\n```\n\nThis will yield the following result (with the [notmyidea][] theme):\n\n![figure](https://github.com/pelican-plugins/avatar/raw/main/avatar-example.png)\n\n[notmyidea]: https://github.com/getpelican/pelican/tree/master/pelican/themes/notmyidea\n\nPage templates work in a similar way:\n\n```html\n{% if page.author_avatar %}\n<div align="center">\n        <img src="{{ page.author_avatar }}">\n</div>\n{% endif %}\n```\n\nTo use in common templates, such as `base.html`, you can do something like this:\n\n```html\n{% if author_avatar %}\n<div align="center">\n        <img src="{{ author_avatar }}">\n</div>\n{% endif %}\n```\n\nOr if you want to support optional overriding of the email address in articles or pages, while still using the global configuration if neither is available:\n\n```html\n{% if article and article.author_avatar %}\n  {% set author_avatar = article.author_avatar %}\n{% elif page and page.author_avatar %}\n  {% set author_avatar = page.author_avatar %}\n{% endif %}\n{% if author_avatar %}\n<div align="center">\n        <img src="{{ author_avatar }}">\n</div>\n{% endif %}\n```\n\nConfiguration\n-------------\n\nThe following variables can be set in the Pelican settings file:\n\n- `AVATAR_AUTHOR_EMAIL`: Site-wide default for the author\'s email address.\n\n- `AVATAR_MISSING`: The default for the missing picture. This can be either a URL (e.g., `"http://example.com/nobody.png"`) or the name of a library of logos (e.g., `"wavatar"`; for the full set of alternatives, see the [Libravatar API](https://wiki.libravatar.org/api/)).\n\n- `AVATAR_SIZE`: The size, in pixels, of the profile picture (it is always square, so the height is equal to the width). If not specified, the default size (80×80) is returned by Libravatar.\n\n- `AVATAR_USE_GRAVATAR`: The plugin looks up avatars via the Libravatar service by default. Searching the Gravatar service can be forced by setting this configuration variable to `True`.\n\nCredits\n-------\n\nInspiration for this plugin came from the [Gravatar plugin](https://github.com/getpelican/pelican-plugins/tree/master/gravatar).\n\nContributing\n------------\n\nContributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].\n\nTo start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.\n\n[existing issues]: https://github.com/pelican-plugins/avatar/issues\n[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html\n\nAcknowledgments\n---------------\n\nThanks to [Justin Mayer][] for helping with migration of this plugin under the Pelican Plugins organization and  to [Troy Curtis][] for adding support for page generator and global generator context and for making improvements in the Poetry workflow.\n\n[Justin Mayer]: https://github.com/justinmayer\n[Troy Curtis]: https://github.com/troycurtisjr\n\nAuthor\n------\n\nCopyright (C) 2015, 2021  Rafael Laboissière (<rafael@laboissiere.net>)\n\nLicense\n-------\n\nThis project is licensed under the AGPL 3.0 license.\n',
    'author': 'Rafael Laboissière',
    'author_email': 'rafael@laboissiere.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pelican-plugins/avatar',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
