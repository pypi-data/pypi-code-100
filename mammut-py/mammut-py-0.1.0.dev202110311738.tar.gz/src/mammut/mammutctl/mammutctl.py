import click
import os


def get_version_number():
    path = os.path.dirname(__file__)
    file_name = path + "/../../../pyproject.toml"
    setup_file = open(file_name, 'r')
    lines = setup_file.read().split('\n')
    version_number_range=[]
    for index, line in enumerate(lines):
        if 'version' in line:
            for letter_index, letter in enumerate(line):
                if letter == '"':
                    version_number_range.append(letter_index)
            return line[version_number_range[0]+1:version_number_range[1]]

@click.command()
@click.version_option(get_version_number())
def main():
    """mammutctl script."""
    click.echo('mammutctl under construction!')
