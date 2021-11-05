from typing import Any, Dict

from algolink.core.analyzer.buildable import BuildableAnalyzer
from algolink.core.objects import Image, RuntimeEnvironment, RuntimeInstance
from .base import DockerEnv
from .builder import DockerBuilder
from .runner import DockerRunner
from algolink.runtime.server import Server


def build_docker_image(name: str, obj, server: Server = None, env: DockerEnv = None, tag: str = 'latest',
                       repository: str = None, force_overwrite: bool = False, **kwargs) -> Image:
    """Build docker image from object

    :param name: name of the resultimg image
    :param obj: obj to build image. must be convertible to Buildable: Model, Pipeline, list of one of those, etc.
    :param server: server to build image with
    :param env: DockerEnv to build in. Default - local docker daemon
    :param tag: image tag
    :param repository: image repository
    :param force_overwrite: wheter to force overwrite existing image
    :parma kwargs: additional arguments for DockerBuilder.build_image
    """
    if server is None:
        try:
            from algolink.ext.flask import FlaskServer
            server = FlaskServer()
        except ImportError:
            raise RuntimeError('cannot use default FlaskServer - flask or flasgger are not installed')
    env = env or DockerEnv()
    source = BuildableAnalyzer.analyze(obj, server=server)
    builder: DockerBuilder = env.get_builder()
    params = builder.create_image(name, env, tag, repository)
    builder.build_image(source, params, env, force_overwrite, **kwargs)
    image = Image(name, source, params=params)
    image.environment = RuntimeEnvironment('temp_env', params=env)
    return image.bind_builder(builder)


def run_docker_instance(image: Image, name: str = None, env: DockerEnv = None,
                        port_mapping: Dict[int, int] = None, instance_kwargs: Dict[str, Any] = None, rm: bool = False,
                        detach: bool = True, **kwargs) -> RuntimeInstance:
    """Create and run docker container

    :param image: image to build from
    :param name: name of the container. defaults to image name
    :param env: DockerEnv to run in. Default - local docker daemon
    :param port_mapping: port mapping for container
    :param instance_kwargs: additional DockerInstance args
    :param rm: wheter to remove container on exit
    :param detach: wheter to detach from container after run
    :param kwargs: additional args for DockerRunner.run
    """
    env = env or DockerEnv()
    name = name or image.name
    runner: DockerRunner = env.get_runner()
    params = runner.create_instance(name, port_mapping, **instance_kwargs or {})
    runner.run(params, image.params, env, rm, detach, **kwargs)
    instance = RuntimeInstance(name, params=params, image_id=image.id).bind_runner(runner)
    instance.environment = RuntimeEnvironment('temp_env', params=env)
    return instance
