import json
from argparse import ArgumentParser

from innotescus import client_factory

def main(*args, **kwargs):
    parser = _build_argparser()
    all_args = parser.parse_args()
    client = client_factory()
    resp = getattr(client, all_args.which)(**all_args)
    print(json.dumps(resp))


def _build_argparser() -> ArgumentParser:
    parser = ArgumentParser()

    subparsers = parser.add_subparsers(title='command', description='')

    hello_world_command = subparsers.add_parser('hello_world')
    # hello_world_command.set_defaults(which='hello_world')

    get_projects_command = subparsers.add_parser('get_projects')
    # get_projects_command.set_defaults(which='get_projects')

    get_projects_by_name_command = subparsers.add_parser('get_projects_by_name')
    get_projects_by_name_command.add_argument('--project-name', dest='project_name')

    create_project_command = subparsers.add_parser('create_project')
    create_project_command.add_argument('--create-project', dest='create_project')

    create_task_command = subparsers.add_parser('create_task')
    create_task_command.add_argument('--project-name', dest='project_name')
    create_task_command.add_argument('--task-name', dest='task_name')
    create_task_command.add_argument('--task-type', dest='task_type')
    create_task_command.add_argument('--data-type', dest='data_type')
    create_task_command.add_argument('--classes', dest='classes')
    create_task_command.add_argument('--datasets', dest='datasets')
    create_task_command.add_argument('--task-description', dest='task_description')
    create_task_command.add_argument('--instructions', dest='instructions')  # noop??
    create_task_command.add_argument('--can-annotator-add-classes', dest='can_annotator_add_classes') # todo: bool

    assign_task_to_datasets = subparsers.add_parser('assign_task_to_datasets')
    assign_task_to_datasets.add_argument('--project-name', dest='project_name')
    assign_task_to_datasets.add_argument('--assignments', dest='assignments')

    upload_annotations_command = subparsers.add_parser('upload_annotations')

    export_command = subparsers.add_parser('export')
    export_command.add_argument('--export-name', dest='export_name')
    export_command.add_argument('--project-name', dest='project_name')
    export_command.add_argument('--annotation-format', dest='annotation_format')
    export_command.add_argument('--export-types', dest='export_types')
    export_command.add_argument('--dataset-names', dest='dataset_names')
    export_command.add_argument('--task-name', dest='task_name')

    download_export_command = subparsers.add_parser('download_export')
    download_export_command.add_argument('--export-name', dest='export_name')
    download_export_command.add_argument('--project-name', dest='project_name')

    get_in_progress_jobs_command = subparsers.add_parser('get_in_progress_jobs')

    get_job_status_command = subparsers.add_parser('get_job_status')
    get_job_status_command.add_argument('--job-id', dest='job_id')

    delete_project_command = subparsers.add_parser('delete_project')
    delete_project_command.add_argument('--project-name', dest='project_name')

    delete_dataset_command = subparsers.add_parser('delete_dataset')
    delete_dataset_command.add_argument('--project-name', dest='project_name')
    delete_dataset_command.add_argument('--dataset-name', dest='dataset_name')

    delete_task_command = subparsers.add_parser('delete_task')
    delete_task_command.add_argument('--project-name', dest='project_name')
    delete_task_command.add_argument('--dataset-name', dest='dataset_name')

    return parser


if __name__ == '__main__':
    main()
