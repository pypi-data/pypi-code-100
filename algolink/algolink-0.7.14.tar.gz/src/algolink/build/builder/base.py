import os
import shutil
from abc import abstractmethod
from contextlib import contextmanager

from algolink.build.provider import PythonProvider
from algolink.core.objects import core
from algolink.utils.fs import get_lib_path
from algolink.utils.log import logger

REQUIREMENTS = 'requirements.txt'
_ALGOLINK_SOURCE = True
# _ALGOLINK_SOURCE defines in which way algolink will be installed inside of the instance. Depending on it's value
# True - means that it will install algolink from PIP
# False - That it will use local algolink installation
# str, representing a path - that it will search for .whl file with algolink package


def algolink_from_pip():
    """
    :return boolen flag if algolink inside image must be installed from pip (or copied local dist instread)"""
    return _ALGOLINK_SOURCE


@contextmanager
def use_local_installation():
    """Context manager that changes docker builder behaviour to copy
    this installation of algolink instead of installing it from pip.
    This is needed for testing and examples"""
    global _ALGOLINK_SOURCE
    tmp = _ALGOLINK_SOURCE
    _ALGOLINK_SOURCE = False
    try:
        yield
    finally:
        _ALGOLINK_SOURCE = tmp


@contextmanager
def use_wheel_installation(path: str):
    """Context manager that changes docker builder behaviour to
    install algolink from wheel.
    This is needed in the case you using algolink from wheel"""
    global _ALGOLINK_SOURCE
    tmp = _ALGOLINK_SOURCE
    _ALGOLINK_SOURCE = path
    try:
        yield
    finally:
        _ALGOLINK_SOURCE = tmp


class BuilderBase:
    """Abstract class for building images from algolink objects"""

    @abstractmethod
    def create_image(self, name: str, environment: 'core.RuntimeEnvironment', **kwargs) -> 'core.Image.Params':
        """Abstract method to create image"""

    @abstractmethod
    def build_image(self, buildable: 'core.Buildable', image: 'core.Image.Params',
                    environment: 'core.RuntimeEnvironment.Params', **kwargs):
        """Abstract method to build image"""

    @abstractmethod
    def delete_image(self, image: 'core.Image.Params', environment: 'core.RuntimeEnvironment.Params', **kwargs):
        """Abstract method to delete image"""

    @abstractmethod
    def image_exists(self, image: 'core.Image.Params', environment: 'core.RuntimeEnvironment.Params', **kwargs):
        """Abstract method to check if image exists"""


class PythonBuildContext:
    """
    Basic class for building python images from algolink objects

    :param provider: A ProviderBase instance to get distribution from
    """

    def __init__(self, provider: PythonProvider):
        self.provider = provider

    def _write_distribution(self, target_dir):
        """
        Writes full distribution to dir
        :param target_dir: target directory to write distribution
        """
        logger.debug('Writing model distribution to "%s"...', target_dir)
        self._write_sources(target_dir)
        self._write_binaries(target_dir)
        self._write_requirements(target_dir)
        self._write_run_script(target_dir)

    def _write_sources(self, target_dir):
        """
        Writes sources to dir
        :param target_dir: target directory to write sources
        """
        for name, content in self.provider.get_sources().items():
            logger.debug('Putting model source "%s" to distribution...', name)
            path = os.path.join(target_dir, name)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w' if isinstance(content, str) else 'wb', encoding='utf8') as src:
                src.write(content)

        pip_algolink = algolink_from_pip()
        if pip_algolink is False:
            logger.debug('Putting AlgoLink sources to distribution as local installation is employed...')
            main_module_path = get_lib_path('.')
            shutil.copytree(main_module_path, os.path.join(target_dir, 'algolink'))
        elif isinstance(pip_algolink, str):
            logger.debug('Putting AlgoLink wheel to distribution as wheel installation is employed...')
            shutil.copy(pip_algolink, target_dir)

    def _write_binaries(self, path):
        """
        Writes binaries to dir
        :param path: target directory to write binaries
        """
        logger.debug('Putting model artifacts to distribution...')
        a = self.provider.get_artifacts()
        a.materialize(path)

    def _write_requirements(self, target_dir):
        """
        Writes requirements.txt to dir
        :param target_dir: target directory to write requirements
        """
        with open(os.path.join(target_dir, REQUIREMENTS), 'w', encoding='utf8') as req:
            requirements = self.provider.get_requirements()
            logger.debug('Auto-determined requirements for model: %s.', requirements.to_pip())
            if algolink_from_pip() is False:
                cwd = os.getcwd()
                try:
                    from setup import setup_args  # FIXME only for development
                    requirements += list(setup_args['install_requires'])
                    logger.debug('Adding AlgoLink requirements as local installation is employed...')
                    logger.debug('Overall requirements for model: %s.', requirements.to_pip())
                finally:
                    os.chdir(cwd)
            req.write('\n'.join(requirements.to_pip()))

    def _write_run_script(self, target_dir):
        """
        Writes run.sh script to dir
        :param target_dir: target directory to script
        """
        with open(os.path.join(target_dir, 'run.sh'), 'w') as sh:
            sh.write('python -c "from algolink import start_runtime; start_runtime()"')
