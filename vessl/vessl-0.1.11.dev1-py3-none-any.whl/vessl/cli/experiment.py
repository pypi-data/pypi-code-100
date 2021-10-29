import os
from typing import List

import click

import vessl
from vessl.cli._base import VesslGroup, vessl_argument, vessl_option
from vessl.cli._util import (
    Endpoint,
    generic_prompter,
    print_data,
    print_logs,
    print_table,
    print_volume_files,
    prompt_choices,
    truncate_datetime,
)
from vessl.cli.organization import organization_name_option
from vessl.cli.project import project_name_option
from vessl.experiment import (
    create_experiment,
    download_experiment_output_files,
    list_distributed_experiment_logs,
    list_experiment_logs,
    list_experiment_output_files,
    list_experiments,
    read_experiment,
)
from vessl.kernel_cluster import list_cluster_nodes, list_clusters, read_cluster
from vessl.kernel_image import list_kernel_images
from vessl.kernel_resource_spec import list_kernel_resource_specs
from vessl.util.constant import (
    FRAMEWORK_TYPE_PYTORCH,
    FRAMEWORK_TYPE_TENSORFLOW,
    FRAMEWORK_TYPES,
    MOUNT_PATH_OUTPUT,
    PROCESSOR_TYPE_GPU,
    PROCESSOR_TYPES,
)


def experiment_name_prompter(
    ctx: click.Context, param: click.Parameter, value: str
) -> str:
    experiments = list_experiments()
    return prompt_choices(
        "Experiment", [(f"{x.name} #{x.number}", x.name) for x in reversed(experiments)]
    )


def cluster_name_prompter(
    ctx: click.Context, param: click.Parameter, value: str
) -> str:
    clusters = list_clusters()
    if not vessl.vessl_api.organization.is_managed_cluster_enabled:
        clusters = filter(lambda x: not x.is_savvihub_managed, clusters)

    cluster = prompt_choices(
        "Cluster",
        [(f"{x.name}", x) for x in clusters],
    )
    ctx.obj["cluster"] = cluster
    return cluster.name


def cluster_name_callback(
    ctx: click.Context, param: click.Parameter, value: str
) -> str:
    if "cluster" not in ctx.obj:
        ctx.obj["cluster"] = read_cluster(value)
    return value


def resource_name_prompter(
    ctx: click.Context, param: click.Parameter, value: str
) -> str:
    cluster = ctx.obj.get("cluster")
    if cluster is None:
        raise click.BadOptionUsage(
            option_name="--cluster",
            message="Cluster (`--cluster`) must be specified before resource (`--resource`).",
        )

    if cluster.is_savvihub_managed:
        resources = list_kernel_resource_specs()
        resource = prompt_choices("Resource", [(x.name, x) for x in resources])
        ctx.obj["processor_type"] = resource.processor_type
        return resource.name


def processor_type_prompter(
    ctx: click.Context, param: click.Parameter, value: str
) -> str:
    cluster = ctx.obj.get("cluster")
    if cluster is None:
        raise click.BadOptionUsage(
            option_name="--cluster",
            message="Cluster (`--cluster`) must be specified before processor type (`--processor-type`).",
        )

    if not cluster.is_savvihub_managed:
        processor_type = prompt_choices("Processor Type", PROCESSOR_TYPES)
        ctx.obj["processor_type"] = processor_type
        return processor_type


def cpu_limit_prompter(
    ctx: click.Context, param: click.Parameter, value: float
) -> float:
    cluster = ctx.obj.get("cluster")
    if cluster is None:
        raise click.BadOptionUsage(
            option_name="--cluster",
            message="Cluster (`--cluster`) must be specified before CPU limit (`--cpu-limit`).",
        )

    if not cluster.is_savvihub_managed:
        return click.prompt("CPUs (in vCPU)", type=click.FLOAT)


def memory_limit_prompter(
    ctx: click.Context, param: click.Parameter, value: float
) -> float:
    cluster = ctx.obj.get("cluster")
    if cluster is None:
        raise click.BadOptionUsage(
            option_name="--cluster",
            message="Cluster (`--cluster`) must be specified before memory limit (`--memory-limit`).",
        )

    if not cluster.is_savvihub_managed:
        return click.prompt("Memory (e.g. 4Gi)", type=click.STRING)


def gpu_type_prompter(ctx: click.Context, param: click.Parameter, value: str) -> str:
    cluster = ctx.obj.get("cluster")
    if cluster is None:
        raise click.BadOptionUsage(
            option_name="--cluster",
            message="Cluster (`--cluster`) must be specified before GPU type (`--gpu-type`).",
        )
    if cluster.is_savvihub_managed:
        return

    processor_type = ctx.obj.get("processor_type")
    if processor_type is None:
        raise click.UsageError(
            message="Processor type must be specified before GPU type (`--gpu-type`).",
        )
    if processor_type == PROCESSOR_TYPE_GPU:
        nodes = list_cluster_nodes(cluster.name)
        return prompt_choices("GPU Type", [x.gpu_product_name for x in nodes])


def gpu_limit_prompter(
    ctx: click.Context, param: click.Parameter, value: float
) -> float:
    cluster = ctx.obj.get("cluster")
    if cluster is None:
        raise click.BadOptionUsage(
            option_name="--cluster",
            message="Cluster (`--cluster`) must be specified before GPU limit (`--gpu-limit`).",
        )
    if cluster.is_savvihub_managed:
        return

    processor_type = ctx.obj.get("processor_type")
    if processor_type is None:
        raise click.UsageError(
            message="Processor type must be specified before GPU limit (`--gpu-limit`).",
        )

    if processor_type == PROCESSOR_TYPE_GPU:
        return click.prompt("GPUs (in vGPU)", type=click.FLOAT)


def image_url_prompter(ctx: click.Context, param: click.Parameter, value: str) -> str:
    processor_type = ctx.obj.get("processor_type")
    if processor_type is None:
        raise click.UsageError(
            message="Processor type must be specified before image URL (`--image-url`).",
        )

    images = list_kernel_images()
    images = [x for x in images if x.processor_type == processor_type]

    return prompt_choices("Image URL", [x.image_url for x in images])


def worker_count_callback(
    ctx: click.Context, param: click.Parameter, value: int
) -> int:
    if value is None:
        value = 1

    if value < 1:
        raise click.BadOptionUsage(
            option_name="--worker-count",
            message="num nodes (`--num-nodes`) must be a positive integer.",
        )

    ctx.obj["worker_count"] = value
    return value


def framework_type_prompter(
    ctx: click.Context, param: click.Parameter, value: str
) -> str:
    worker_count = ctx.obj.get("worker_count")
    if worker_count == 1:
        return ""

    framework_type = prompt_choices("Processor Type", FRAMEWORK_TYPES)
    if framework_type == FRAMEWORK_TYPE_TENSORFLOW:
        raise click.BadOptionUsage(
            option_name="--framework-type",
            message="Only PyTorch distributed experiment is supported currently.",
        )
    return framework_type


@click.command(name="experiment", cls=VesslGroup)
def cli():
    pass


@cli.vessl_command()
@vessl_argument(
    "name", type=click.STRING, required=True, prompter=experiment_name_prompter
)
@organization_name_option
@project_name_option
def read(name: str):
    experiment = read_experiment(experiment_name_or_number=name)

    distributed_spec = "None"
    if experiment.is_distributed:
        if experiment.distributed_spec.framework_type == FRAMEWORK_TYPE_PYTORCH:
            distributed_spec = {
                "Framework Type": experiment.distributed_spec.framework_type,
                "PyTorch Spec": {
                    "Worker count": experiment.distributed_spec.pytorch_spec.worker_replicas,
                },
            }
        elif experiment.distributed_spec.framework_type == FRAMEWORK_TYPE_TENSORFLOW:
            distributed_spec = {
                "Framework Type": experiment.distributed_spec.framework_type,
                "TensorFlow Spec": experiment.distributed_spec.tensorflow_spec,
            }

    kernel_image = "None"
    if experiment.kernel_image:
        kernel_image = {
            "Name": experiment.kernel_image.name,
            "URL": experiment.kernel_image.image_url,
        }

    resource_spec = "None"
    if experiment.kernel_resource_spec:
        resource_spec = {
            "Name": experiment.kernel_resource_spec.name,
            "CPU Type": experiment.kernel_resource_spec.cpu_type,
            "CPU Limit": experiment.kernel_resource_spec.cpu_limit,
            "Memory Limit": experiment.kernel_resource_spec.memory_limit,
            "GPU Type": experiment.kernel_resource_spec.gpu_type,
            "GPU Limit": experiment.kernel_resource_spec.gpu_limit,
        }

    print_data(
        {
            "ID": experiment.id,
            "Number": experiment.number,
            "Name": experiment.name,
            "Distributed": experiment.is_distributed,
            "Distributed Spec": distributed_spec,
            "Local": experiment.is_local,
            "Status": experiment.status,
            "Created": truncate_datetime(experiment.created_dt),
            "Message": experiment.message,
            "Kernel Image": kernel_image,
            "Resource Spec": resource_spec,
            "Start command": experiment.start_command,
        }
    )
    print(
        f"For more info: {Endpoint.experiment.format(experiment.organization.name, experiment.project.name, experiment.number)}"
    )


@cli.vessl_command()
@organization_name_option
@project_name_option
def list():
    experiments = list_experiments()
    print_table(
        experiments,
        ["ID", "Name", "Distributed", "Status", "Created", "Message"],
        lambda x: [
            x.id,
            x.name,
            x.is_distributed,
            x.status,
            truncate_datetime(x.created_dt),
            x.message,
        ],
    )


cluster_option = vessl_option(
    "-c",
    "--cluster",
    type=click.STRING,
    required=True,
    prompter=cluster_name_prompter,
    callback=cluster_name_callback,
    help="Must be specified before resource-related options (`--resource`, `--processor`, ...).",
)
command_option = vessl_option(
    "-x",
    "--command",
    type=click.STRING,
    required=True,
    prompter=generic_prompter("Start command"),
    help="Start command to execute in experiment container.",
)
resource_option = vessl_option(
    "-r",
    "--resource",
    type=click.STRING,
    prompter=resource_name_prompter,
    help="Resource type to run experiment (for managed cluster only).",
)
processor_type_option = vessl_option(
    "--processor-type",
    type=click.Choice(("CPU", "GPU")),
    prompter=processor_type_prompter,
    help="CPU or GPU (for custom cluster only).",
)
cpu_limit_option = vessl_option(
    "--cpu-limit",
    type=click.FLOAT,
    prompter=cpu_limit_prompter,
    help="Number of vCPUs (for custom cluster only).",
)
memory_limit_option = vessl_option(
    "--memory-limit",
    type=click.STRING,
    prompter=memory_limit_prompter,
    help="Memory limit (e.g. 4Gi) (for custom cluster only).",
)
gpu_type_option = vessl_option(
    "--gpu-type",
    type=click.STRING,
    prompter=gpu_type_prompter,
    help="GPU type such as Tesla-K80 (for custom cluster only).",
)
gpu_limit_option = vessl_option(
    "--gpu-limit",
    type=click.INT,
    prompter=gpu_limit_prompter,
    help="Number of GPU cores (for custom cluster only).",
)
image_url_option = vessl_option(
    "-i",
    "--image-url",
    type=click.STRING,
    prompter=image_url_prompter,
    help="Kernel docker image URL",
)
message_option = click.option("-m", "--message", type=click.STRING)
termination_protection_option = click.option("--termination-protection", is_flag=True)
env_var_option = click.option(
    "-e",
    "--env-var",
    type=click.STRING,
    multiple=True,
    help="Environment variables. Format: [key]=[value], ex. `--env-var PORT=8080`.",
)
dataset_option = click.option(
    "--dataset",
    type=click.STRING,
    multiple=True,
    help="Dataset mounts. Format: [mount_path]:[dataset_name]@[optional_dataset_version], ex. `--dataset /input:mnist@3bcd5f`.",
)
git_ref_option = click.option(
    "--git-ref",
    type=click.STRING,
    multiple=True,
    help="Git repository mounts. Format: [mount_path]:github/[organization]/[repository]/[optional_commit], ex. `--git-ref /home/vessl/examples:github/savvihub/examples/3cd23dd`.",
)
git_diff_option = click.option(
    "--git-diff",
    type=click.STRING,
    help="Git diff file mounts. Format: [mount_path]:[volume_file_path]]. This option is used only for reproducing existing experiments.",
)
archive_file_option = click.option(
    "--archive-file",
    type=click.STRING,
    help="Local archive file mounts. Format: [mount_path]:[archive_file_path]]. This option is used only for reproducing existing experiments.",
)
root_volume_size_option = click.option("--root-volume-size", type=click.STRING)
working_dir_option = click.option(
    "--working-dir", type=click.STRING, help="Defaults to `/home/vessl/`."
)
output_dir_option = click.option(
    "--output-dir",
    type=click.STRING,
    default=MOUNT_PATH_OUTPUT,
    help="Directory to store experiment output files. Defaults to `/output`.",
)
worker_count_option = vessl_option(
    "--worker-count",
    type=click.INT,
    callback=worker_count_callback,
    help="The number of nodes to run an experiment. Defaults to 1",
)
framework_type_option = vessl_option(
    "--framework-type",
    type=click.STRING,
    prompter=framework_type_prompter,
    help="Framework type option. Defaults to `pytorch`.",
)


@cli.vessl_command()
@cluster_option
@command_option
@resource_option
@processor_type_option
@cpu_limit_option
@memory_limit_option
@gpu_type_option
@gpu_limit_option
@image_url_option
@message_option
@termination_protection_option
@env_var_option
@dataset_option
@git_ref_option
@git_diff_option
@archive_file_option
@root_volume_size_option
@working_dir_option
@output_dir_option
@organization_name_option
@project_name_option
@worker_count_option
@framework_type_option
def create(
    cluster: str,
    command: str,
    resource: str,
    processor_type: str,
    cpu_limit: float,
    memory_limit: str,
    gpu_type: str,
    gpu_limit: int,
    image_url: str,
    message: str,
    termination_protection: bool,
    env_var: List[str],
    dataset: List[str],
    git_ref: List[str],
    git_diff: str,
    archive_file: str,
    root_volume_size: str,
    working_dir: str,
    output_dir: str,
    worker_count: int,
    framework_type: str,
):
    experiment = create_experiment(
        cluster_name=cluster,
        start_command=command,
        kernel_resource_spec_name=resource,
        processor_type=processor_type,
        cpu_limit=cpu_limit,
        memory_limit=memory_limit,
        gpu_type=gpu_type,
        gpu_limit=gpu_limit,
        kernel_image_url=image_url,
        message=message,
        termination_protection=termination_protection,
        env_vars=env_var,
        dataset_mounts=dataset,
        git_ref_mounts=git_ref,
        git_diff_mount=git_diff,
        archive_file_mount=archive_file,
        root_volume_size=root_volume_size,
        working_dir=working_dir,
        output_dir=output_dir,
        worker_count=worker_count,
        framework_type=framework_type,
    )
    print(
        f"Created '{experiment.name}'.\n"
        f"For more info: {Endpoint.experiment.format(experiment.organization.name, experiment.project.name, experiment.number)}"
    )


worker_number_option = vessl_option(
    "--worker-number",
    type=click.INT,
    default=0,
    help="Worker number (for distributed experiment only).",
)


@cli.vessl_command()
@vessl_argument(
    "name", type=click.STRING, required=True, prompter=experiment_name_prompter
)
@click.option(
    "--tail",
    type=click.INT,
    default=200,
    help="Number of lines to display (from the end).",
)
@organization_name_option
@project_name_option
@worker_number_option
def logs(
    name: str,
    tail: int,
    worker_number: int,
):
    experiment = read_experiment(experiment_name_or_number=name)
    if experiment.is_distributed:
        logs = list_distributed_experiment_logs(
            experiment_name=name, tail=tail, worker_number=worker_number
        )

        print_logs(logs)
    else:
        logs = list_experiment_logs(experiment_name=name, tail=tail)
        print_logs(logs)
    print(f"Displayed last {len(logs)} lines of '{name}'.")


@cli.vessl_command()
@vessl_argument(
    "name", type=click.STRING, required=True, prompter=experiment_name_prompter
)
@click.option("-r", "--recursive", is_flag=True)
@organization_name_option
@project_name_option
@worker_number_option
def list_output(
    name: str,
    recursive: bool,
    worker_number: int,
):
    files = list_experiment_output_files(
        experiment_name=name,
        need_download_url=False,
        recursive=recursive,
        worker_number=worker_number,
    )
    print_volume_files(files)


@cli.vessl_command()
@vessl_argument(
    "name", type=click.STRING, required=True, prompter=experiment_name_prompter
)
@click.option(
    "-p",
    "--path",
    type=click.Path(),
    default=os.path.join(os.getcwd(), "output"),
    help="Path to store downloads. Defaults to `./output`.",
)
@organization_name_option
@project_name_option
@worker_number_option
def download_output(
    name: str,
    path: str,
    worker_number: int,
):
    download_experiment_output_files(
        experiment_name=name,
        dest_path=path,
        worker_number=worker_number,
    )
    print(f"Downloaded experiment to {path}.")
