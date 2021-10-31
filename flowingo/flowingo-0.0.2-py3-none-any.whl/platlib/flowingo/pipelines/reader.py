import glob
import pathlib
from typing import Any, Dict, Generator, List, Set, Tuple, Union

import yaml

try:
    YamlLoader = yaml.CSafeLoader
except AttributeError:  # pragma: nocover
    # System does not have libyaml
    YamlLoader = yaml.SafeLoader


def read_yml(filename: Union[str, pathlib.Path]) -> Dict[str, Any]:
    filename = pathlib.Path(filename)
    assert filename.exists(), f'file "{filename.absolute()}" not exists'

    with open(filename, 'r') as f:
        content = yaml.load(f, Loader=YamlLoader)

    return content


def read_all_tasks(tasks_folder: pathlib.Path) -> Dict[str, Any]:
    tasks_files = [
        i for i in glob.glob(str(tasks_folder / '*'), recursive=True) if i.endswith('.yaml') or i.endswith('.yml')
    ]

    tasks: Dict[str, Any] = {}
    for filename in tasks_files:
        current_tasks = read_task(tasks_folder, filename)
        tasks.update(current_tasks['tasks'])

    return tasks


def read_task(tasks_folder: pathlib.Path, filename: str) -> Dict[str, Any]:
    return read_yml(tasks_folder / filename)


def _get_all_sub_pipelines(pipeline_tasks_content: List[Dict[str, Any]]) -> Set[str]:
    sub_pipelines = set()

    for task in pipeline_tasks_content:
        if 'if' in task:
            for value_inner in task['values'].values():
                if not value_inner:
                    pass
                elif isinstance(value_inner, str):
                    sub_pipelines.add(value_inner)
                elif isinstance(value_inner, list):
                    sub_pipelines.update(_get_all_sub_pipelines(value_inner))
                else:  # pragma: nocover
                    raise RuntimeError('')
        elif 'chain' in task:
            inner = task['chain']
            if isinstance(inner, str):
                sub_pipelines.add(inner)
            elif isinstance(inner, list):
                sub_pipelines.update(_get_all_sub_pipelines(inner))
            else:  # pragma: nocover
                raise RuntimeError('')
        elif 'group' in task:
            sub_pipelines.update(_get_all_sub_pipelines(task['group']))

    return sub_pipelines


def _read_related_pipelines(pipelines_folder: pathlib.Path, current_filename: str,
                            pipeline_visited: Dict[str, bool],
                            pipelines: Dict[str, Any]) -> None:
    pipeline_visited[current_filename] = False
    if current_filename not in pipelines:
        path = pipelines_folder / current_filename
        assert path.exists(), f'Pipeline file {path.absolute()} must exists'

        pipelines[current_filename] = read_yml(str(path.absolute()))
    pipeline_content = pipelines[current_filename]

    for sub_pipeline_filename in _get_all_sub_pipelines(pipeline_content['tasks']):
        if sub_pipeline_filename not in pipeline_visited:  # if not start or end
            _read_related_pipelines(pipelines_folder, sub_pipeline_filename, pipeline_visited, pipelines)
        else:  # if already started or end
            raise RuntimeError('cycle dependencies')  # TODO: customize exceptions

    pipeline_visited[current_filename] = True


def read_related_pipelines(pipelines_folder: pathlib.Path, filename: str) -> Dict[str, Any]:
    pipeline_visited: Dict[str, bool] = {}
    pipelines: Dict[str, Any] = {}

    _read_related_pipelines(pipelines_folder, filename, pipeline_visited, pipelines)

    return pipelines


def read_pipeline(pipelines_folder: pathlib.Path, filename: str) -> Dict[str, Any]:
    return read_yml(pipelines_folder / filename)
