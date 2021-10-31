import pathlib
from typing import Any, Dict, Optional, Union

import yaml

from flowingo.pipelines.reader import _read_related_pipelines
from flowingo.pipelines.validation import validate_pipelines


def write_yml(filename: Union[str, pathlib.Path], content: Dict[str, Any]):
    filename = pathlib.Path(filename)
    filename.parent.mkdir(exist_ok=True)

    with open(filename.absolute(), 'w') as f:
        yaml.dump(content, f)


def write_pipeline(pipelines_folder: pathlib.Path, filename: str, pipeline: Dict[str, Any], tasks_folder: Optional[pathlib.Path] = None):
    # Try to read all related pipelines
    pipeline_visited: Dict[str, bool] = {}
    pipelines: Dict[str, Any] = {filename: pipeline}  # preload new pipeline
    _read_related_pipelines(pipelines_folder, filename, pipeline_visited, pipelines)

    # Validate pipeline content (only new)
    is_valid = validate_pipelines(pipelines_folder, {filename: pipeline}, tasks_folder=tasks_folder)
    if not is_valid:
        raise RuntimeError('Validation exception')

    # Write itself
    return write_yml(pipelines_folder / filename, pipeline)
