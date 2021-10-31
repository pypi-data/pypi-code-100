import pathlib

import click

from flowingo.pipelines import validate_pipeline


@click.group()
def pipeline():
    """pipeline executable function"""
    pass


@pipeline.command()
@click.argument('pipeline_folder', type=click.Path(exists=True, file_okay=False, readable=True))
@click.argument('filename', type=click.Path())
def validate(pipeline_folder: str, filename: str):
    """manager executable function"""
    pipeline_folder = pathlib.Path(pipeline_folder)
    path = pipeline_folder / filename

    if not path.exists():
        print(f'pipeline {filename} NOT exists!')
        exit(2)

    if path.suffix not in ['.yaml', '.yml']:
        print(f'{filename} has wrong extension {path.suffix} (Can be .yaml or .yml)')
        exit(1)

    is_valid = validate_pipeline(pipeline_folder, filename)

    if not is_valid:
        print(f'pipeline {filename} is NOT valid!')
        exit(1)

    print(f'pipeline {filename} is valid!')
    exit(0)
