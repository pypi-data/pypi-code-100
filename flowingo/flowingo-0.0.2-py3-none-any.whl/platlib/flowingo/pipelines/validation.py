import pathlib
import warnings
from typing import Any, Dict, List, Optional

import yamale

from flowingo.pipelines.reader import read_all_tasks, read_related_pipelines, read_task

pipeline_schema_path = pathlib.Path(__file__).parent / 'schemas' / 'pipeline_schema.yml'
assert pipeline_schema_path.exists(), 'pipeline_schema.yml have to exist'
tasks_schema_path = pathlib.Path(__file__).parent / 'schemas' / 'tasks_schema.yml'
assert tasks_schema_path.exists(), 'tasks_schema.yml have to exist'


def validate_task(tasks_folder: pathlib.Path, filename: str) -> bool:
    task_path = tasks_folder / filename
    if not task_path.exists():
        return False

    task = read_task(tasks_folder, filename)

    # validate with schema
    schema = yamale.make_schema(tasks_schema_path.absolute())

    try:
        yamale.validate(schema, [(task, task_path)], strict=True, _raise_error=True)
    except yamale.YamaleError as e:
        print(e)
        return False

    return True


def _validate_pipeline_tasks(pipeline_tasks_content: List[Dict[str, Any]], tasks: Dict[str, Any]):
    for task in pipeline_tasks_content:
        if 'task' in task:
            name = task['task']

            if name not in tasks:
                raise RuntimeError(f'No such task `{name}`')  # TODO: customize errors

            if not tasks[name] or isinstance(tasks[name], str) or 'parameters' not in task:
                continue

            parameters = task['parameters']
            current_task_parameters = tasks[name]['parameters']
            for key, value in parameters.items():
                if key not in current_task_parameters:
                    raise RuntimeError(f'No such parameter `{key}` for task `{name}`')  # TODO: customize errors

                if type(value).__name__ != current_task_parameters[key]:
                    raise RuntimeError(f'Parameter `{key}` for task `{name}` has wrong type <{type(value).__name__}> (expected <{current_task_parameters[key]}>)')  # TODO: customize errors

        elif 'if' in task:
            for value_inner in task['values'].values():
                if isinstance(value_inner, list):
                    _validate_pipeline_tasks(value_inner, tasks)

        elif 'chain' in task:
            inner = task['chain']
            if isinstance(inner, list):
                _validate_pipeline_tasks(inner, tasks)

        elif 'group' in task:
            _validate_pipeline_tasks(task['group'], tasks)


def validate_pipelines(pipelines_folder: pathlib.Path, pipelines: Dict[str, Dict[str, Any]], tasks_folder: Optional[pathlib.Path] = None) -> bool:
    if not tasks_folder:
        warnings.warn(
            "running validation without `tasks_folder` will NOT validate used tasks",
            UserWarning
        )

    # validate with schema
    schema = yamale.make_schema(pipeline_schema_path.absolute())

    # read all tasks
    tasks = read_all_tasks(tasks_folder) if tasks_folder else None

    # validate each pipeline
    for pipeline_filename, pipeline in pipelines.items():
        try:
            yamale.validate(schema, [(pipeline, pipelines_folder/pipeline_filename)], strict=True, _raise_error=True)
        except yamale.YamaleError as e:
            print(e)
            return False

        # validate task names and parameters
        if tasks:
            try:
                _validate_pipeline_tasks(pipeline['tasks'], tasks)
            except RuntimeError as e:
                print(e)
                return False

    return True


def validate_pipeline(pipelines_folder: pathlib.Path, filename: str, tasks_folder: Optional[pathlib.Path] = None) -> bool:
    pipeline_path = pipelines_folder / filename
    if not pipeline_path.exists():
        return False

    try:
        # extract all sub-pipelines
        pipelines = read_related_pipelines(pipelines_folder, filename)
    except Exception as e:
        # sub-pipelines not exist, or cyclic dependencies
        print(e)
        return False

    return validate_pipelines(pipelines_folder, pipelines, tasks_folder=tasks_folder)
