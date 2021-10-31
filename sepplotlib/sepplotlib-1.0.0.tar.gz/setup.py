# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sepplotlib']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4.3,<4.0.0', 'pandas>=1.3.4,<2.0.0', 'seaborn>=0.11.2,<0.12.0']

setup_kwargs = {
    'name': 'sepplotlib',
    'version': '1.0.0',
    'description': 'Separation plots for binary classification problems',
    'long_description': '# sepplotlib\n\n> Separation plots for binary classification problems.\n\n## Credits\n> The one-dimensional separation plot is adapted from code originally produced by [Brian Greenhill, Michael D. Ward, and Audrey Sacks](https://onlinelibrary.wiley.com/doi/full/10.1111/j.1540-5907.2011.00525.x). \nThe bi-separation plot and model criticism plot are adapted from code originally produced by [Michael Colaresi and Zuhaib Mahmood](https://journals.sagepub.com/doi/10.1177/0022343316682065).\n\n## Installation\n\n`pip install sepplotlib` to install.\n\n\n## Example usage\n\nPlease see the accompanied notebook for an example using mock data.\n\nThe included figures are objects that expect a pandas DataFrame and strings for the relevant columns. To generate a one-dimensional separation plot for instance, simply run:\n\n```python\nimport sepplotlib as spl\nspl.SeparationPlot(\n    df=df,\n    y_true="y_true",\n    y_pred="y_pred",\n    title="Example"\n)\n```\n\n<img src="https://user-images.githubusercontent.com/31345940/139453276-2caf6b1c-087f-40a9-baa2-2c3fc8f79ab2.png" width="500">\n\nSimilarly to generate a model criticism plot:\n\n```python\nimport sepplotlib as spl\nspl.ModelCriticismPlot(\n    df=df,\n    y_true="y_true",\n    y_pred="y_pred",\n    lab="lab",\n    title="Example"\n)\n```\n\n<img src="https://user-images.githubusercontent.com/31345940/139453840-e9469065-8a67-42d7-81fc-61dac823df32.png" width="400">\n\nAnd finally, to generate a two-dimensional, bi-separation plot:\n\n```python\nimport sepplotlib as spl\nspl.BiseparationPlot(\n    df=df,\n    x="y_pred_a",\n    y="y_pred_b",\n    obs="y_true",\n    lab="lab",\n    title="Example",\n)\n```\n\n<img src="https://user-images.githubusercontent.com/31345940/139453518-83a4ad72-ffba-442c-816c-35902fcaf5b1.png" width="400">\n\nPlease run `help` on any of these classes to learn what can be customized (e.g. `help(spl.SeparationPlot))`).\n',
    'author': 'Remco Bastiaan Jansen',
    'author_email': 'r.b.jansen.uu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
