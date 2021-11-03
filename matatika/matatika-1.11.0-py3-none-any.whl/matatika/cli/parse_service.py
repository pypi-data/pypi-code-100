# pylint: disable=too-many-locals

"""Parse Service"""

# standard
from datetime import datetime
import re
import uuid
import os
import yaml
# external
from nbconvert import MarkdownExporter
from traitlets.config import Config
# local
from matatika.dataset import Dataset
from matatika.channel import Channel
from matatika.types import Resource


def parse_yaml(user_yaml_file, dataset_alias, file_ext):
    """Yaml file parsing"""

    yaml_files = []

    with open(user_yaml_file, 'r', encoding='utf-8') as file:
        yaml_file = yaml.safe_load(file)

        if yaml_file.get('version') == "datasets/v0.2":
            _, tail = os.path.split(user_yaml_file)
            dataset_alias = dataset_alias or tail[:-len(file_ext)]
            file_dict = {dataset_alias: yaml_file}
            yaml_type = Resource.DATASET
        elif yaml_file.get('version') == "channels/v0.1":
            file_dict = {yaml_file.get('name'): yaml_file}
            yaml_type = Resource.CHANNEL
        else:
            file_dict = yaml_file['datasets']
            yaml_type = Resource.DATASET

    if yaml_type == Resource.DATASET:
        if len(file_dict) > 1 and dataset_alias:
            return None, yaml_type
        for alias in file_dict:
            file_dict[alias].update({'alias': dataset_alias or alias})
            dataset = Dataset.from_dict(file_dict[alias])
            yaml_files.append(dataset)

    if yaml_type == Resource.CHANNEL:
        for channel_name in file_dict:
            channel = Channel.from_dict(file_dict[channel_name])
            yaml_files.append(channel)

    return yaml_files, yaml_type



def parse_notebook(dataset_file, dataset_alias, file_ext):
    """Notebook file parsing"""
    datasets = []
    config = Config()
    config.TemplateExporter.exclude_output_prompt = True
    config.TemplateExporter.exclude_input = True
    config.TemplateExporter.exclude_input_prompt = True
    config.ExtractOutputPreprocessor.enabled = False
    md_exporter = MarkdownExporter(config=config)
    md_str, _resources = md_exporter.from_file(dataset_file)

    match = re.search(r'#+\s(.+)', md_str)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    default_title = f"Generated Report ({timestamp})"
    dataset_title = match.group(1) if match else default_title
    _, tail = os.path.split(dataset_file)

    dataset_alias = dataset_alias or tail[:-len(file_ext)]

    dataset = Dataset.from_dict({
        'id': str(uuid.uuid4()),
        'title': dataset_title,
        'description': md_str,
        'alias': dataset_alias
    })
    datasets.append(dataset)
    return datasets
