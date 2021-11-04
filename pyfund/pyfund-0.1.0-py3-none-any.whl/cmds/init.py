import click
import toml

from pyfund import __cfg_path__


@click.command()
@click.argument('path')
def init(path):
    """指定数据目录，默认home目录下。
    """
    with open(__cfg_path__, 'w') as f:
        toml.dump({'data_path':path}, f)
    print(__cfg_path__)