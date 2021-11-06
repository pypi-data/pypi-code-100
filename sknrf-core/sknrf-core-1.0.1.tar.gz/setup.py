import os
import sys
import shutil
import pathlib
from distutils.dir_util import copy_tree
from distutils.command.clean import clean as _clean
from distutils.command.config import config as _config
from distutils.command.build import build as _build
from distutils.command.build_clib import build_clib as _build_clib
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
from distutils.command.install import install as _install
from distutils.command.install_lib import install_lib as _install_lib
from distutils.command.install_data import install_data as _install_data
from distutils.command.upload import upload as _upload
from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from distutils.core import Command
from subprocess import Popen

root = os.path.abspath(os.path.dirname(__file__))
build_root = os.sep.join((root, "build"))
doc_root = os.sep.join((root, "doc"))

# resources
if sys.platform == "win32":
    data_root = os.sep.join((os.getenv("APPDATA"), "sknrf"))
elif sys.platform == "darwin":
    data_root = os.sep.join((os.path.expanduser("~"), ".config", "sknrf"))
elif sys.platform == "linux" or sys.platform == "linux2":
    data_root = os.sep.join((os.path.expanduser("~"), ".config", "sknrf"))
else:
    raise (OSError, "Unsupported Platform")

# src
with open('sknrfconfig.h') as fid:
    for line in fid:
        if line.startswith('#define SKNRF_VERSION_MAJOR'):
            SKNRF_VERSION_MAJOR = int(line.strip().split(' ')[-1])
        elif line.startswith('#define SKNRF_VERSION_MINOR'):
            SKNRF_VERSION_MINOR = int(line.strip().split(' ')[-1])
        elif line.startswith('#define SKNRF_VERSION_PATCH'):
            SKNRF_VERSION_PATCH = int(line.strip().split(' ')[-1])
        else:
            pass
    VERSION = "%d.%d.%d" % (SKNRF_VERSION_MAJOR, SKNRF_VERSION_MINOR, SKNRF_VERSION_PATCH)


def system_cmd(command, wait=True, cwd=root):
    command = command if isinstance(command, str) else " ".join(command)
    print(command)
    process = Popen(command, shell=True, stdout=sys.stdout, cwd=cwd)
    if wait:
        process.wait()
    return process


class clean(_clean):

    def has_pure_modules(self):
        return True

    def has_c_libraries(self):
        return True

    def has_ext_modules(self):
        return False

    def has_scripts(self):
        return True

    sub_commands = [('clean_clib',    has_c_libraries),
                    ('clean_py',      has_pure_modules),
                    ('clean_doc',     has_scripts),
                    ]

    def run(self):
        # Run all relevant sub-commands.  This will be some subset of:
        #  - clean_clib     - standalone C libraries
        #  - clean_py       - pure Python modules
        #  - clean_doc      - documentation
        for cmd_name in self.get_sub_commands():
            self.run_command(cmd_name)


class clean_clib(_config):
    description = "Clean C/C++ build directory"
    user_options = []
    boolean_options = []
    help_options = []

    def initialize_options(self):
        super().initialize_options()

    def finalize_options(self):
        super().finalize_options()

    def run(self):
        bld = pathlib.Path().absolute() / "build"
        cwd = bld / "lib"

        if cwd.exists():
            system_cmd('xargs rm < install_manifest.txt', cwd=cwd)

        # rm -rf build
        if bld.exists():
            shutil.rmtree(str(bld))


class clean_py(_config):
    description = "Clean Python dist directory"
    user_options = []
    boolean_options = []
    help_options = []

    def initialize_options(self):
        super().initialize_options()

    def finalize_options(self):
        super().finalize_options()

    def run(self):
        dst = pathlib.Path().absolute() / "dist"

        # rm -rf dist
        if dst.exists():
            shutil.rmtree(str(dst))


class clean_doc(_config):
    description = "Clean Python doc directory"
    user_options = []
    boolean_options = []
    help_options = []

    def initialize_options(self):
        super().initialize_options()

    def finalize_options(self):
        super().finalize_options()

    def run(self):
        bld = pathlib.Path().absolute() / "doc" / "build"
        api = pathlib.Path().absolute() / "doc" / "source" / "api"

        # rm -rf doc/build
        if bld.exists():
            shutil.rmtree(str(bld))

        # rm -rf doc/source/api
        if api.exists():
            shutil.rmtree(str(api))


class config(_config):

    # -- Predicates for the sub-command list ---------------------------

    def has_pure_modules(self):
        return False

    def has_c_libraries(self):
        return True

    def has_ext_modules(self):
        return False

    def has_scripts(self):
        return False

    sub_commands = [('config_py',      has_pure_modules),
                    ('config_clib',    has_c_libraries),
                    ('config_ext',     has_ext_modules),
                    ('config_scripts', has_scripts),
                    ]

    def run(self):
        # Run all relevant sub-commands.  This will be some subset of:
        #  - config_py      - pure Python modules
        #  - config_clib    - standalone C libraries
        #  - config_ext     - Python extensions
        #  - config_scripts - (Python) scripts
        for cmd_name in self.get_sub_commands():
            self.run_command(cmd_name)


class config_clib(_config):
    description = "Configure C/C++ Libraries"
    user_options = [
        ('debug', 'g', "debug mode"),
        ('force', 'f', "forcibly configure everything (ignore file timestamps)"),
        ('cmake=', 'k', "cmake config options"),
    ]
    boolean_options = ["debug", "force"]
    help_options = []

    def initialize_options(self):
        super().initialize_options()
        self.debug = False
        self.force = False
        self.cmake = None

    def finalize_options(self):
        super().finalize_options()
        self.force = False if self.force is None else self.force
        config = 'Debug' if self.debug else 'Release'
        self.cmake = '-G"Ninja" -DCMAKE_BUILD_TYPE=' + config if self.cmake is None else self.cmake

    def run(self):
        cwd = pathlib.Path().absolute()
        bld = pathlib.Path().absolute() / "build" / "lib"
        doc = pathlib.Path().absolute() / "doc"

        # rm -rf build ; mkdir build ; cd build
        if self.force and bld.exists():
            shutil.rmtree(str(bld))
        bld.mkdir(parents=True, exist_ok=True)
        os.chdir(str(bld))

        shutil.copyfile(os.sep.join((str(cwd), "sknrf.yml")), os.sep.join((str(doc), "sknrf.yml")))
        system_cmd(['cmake', str(cwd), self.cmake], cwd=bld)  # configure: 'cmake ..'


class build(_build):

    # -- Predicates for the sub-command list ---------------------------

    def has_pure_modules(self):
        return self.distribution.has_pure_modules()

    def has_c_libraries(self):
        return True

    def has_ext_modules(self):
        return self.distribution.has_ext_modules()

    def has_scripts(self):
        return self.distribution.has_scripts()

    sub_commands = [('build_py',      has_pure_modules),
                    ('build_clib',    has_c_libraries),
                    ('build_ext',     has_ext_modules),
                    ('build_scripts', has_scripts), ]


class build_clib(_build_clib):
    description = "Build C/C++ Libraries"
    user_options = _build_clib.user_options + [
        ('cmake=', 'k', "cmake build options"),
    ]

    def initialize_options(self):
        super().initialize_options()
        self.cmake = None

    def finalize_options(self):
        super().finalize_options()
        config = 'Debug' if self.debug else 'Release'
        self.cmake = '--config {:s}'.format(config) if self.cmake is None else self.cmake

    def run(self):
        bld = pathlib.Path().absolute() / "build" / "lib"
        system_cmd(['cmake', '--build', str(bld), self.cmake], cwd=build_root)  # make: 'make' to build the project


class install(_install):

    def has_clib(self):
        return True

    def has_data(self):
        return True

    def has_doc(self):
        return True

    sub_commands = [('install_clib',     has_clib),
                    ('install_doc',     has_doc),
                    ('install_data',     has_data), ] + _install.sub_commands


class install_clib(_install_lib):
    description = "Install C/C++ Libraries"
    user_options = _install_lib.user_options + [
        ('cmake=', 'k', "cmake install options"),
    ]

    def initialize_options(self):
        super().initialize_options()
        self.cmake = None

    def finalize_options(self):
        super().finalize_options()
        self.cmake = '--prefix "${CONDA_PREFIX}"' if self.cmake is None else self.cmake

    def run(self):
        bld = pathlib.Path().absolute() / "build" / "lib"
        system_cmd(['cmake', '--install', str(bld), self.cmake], cwd=build_root)  # install:'make install'


class install_doc(Command):
    description = "Build HTML Documentation and save in ./doc/build/html directory."
    user_options = [
        ('force', 'f', "clean the documentation folder."),
        ('api', 'a', "build programmable api."),
        ('html', 'w', "build html documentation."),
    ]
    boolean_options = ['clean', 'api', 'html']
    help_options = []

    def initialize_options(self):
        self.force = False

    def finalize_options(self):
        pass

    def run(self):
        self.force = False if self.force is None else self.force
        if self.force:
            system_cmd("make clean", cwd=doc_root)
        system_cmd("make api", cwd=doc_root)
        system_cmd("make html", cwd=doc_root)


class install_data(_install_data):
    description = "Install application config data from ./sknrf/data"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        dirname = os.sep.join((root, "sknrf", "data", "datagroups"))
        for filename in os.listdir(dirname):
            if filename != ".gitignore":
                os.remove(os.path.join(dirname, filename))
        if not os.path.exists(data_root):
            shutil.copytree(os.sep.join((root, "sknrf", "data")), data_root)
            print("Installed application config data to %s" % (data_root,))
        else:
            print("Directory application config data already exists")


class bdist_wheel(_bdist_wheel):
    def finalize_options(self):
        _bdist_wheel.finalize_options(self)
        self.root_is_pure = False
        self.py_limited_api = "cp37"


class upload(_upload):

    def has_pypi(self):
        return True

    def has_doc(self):
        return True

    sub_commands = [('upload_pypi',    has_pypi),
                    ('upload_doc',     has_doc)] + _install.sub_commands

    def run(self):
        # Run all sub-commands (at least those that need to be run)
        for cmd_name in self.get_sub_commands():
            self.run_command(cmd_name)


class upload_pypi(_upload):

    description = "Upload source code to pypi."
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


class upload_doc(Command):

    description = "Upload latest doc from ./doc/build/ directory."
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        system_cmd("rsync -a --delete ${HOME}/repos/sknrf-core/doc/build/html/ scikitno@scikit-nonlinear.org:/home/scikitno/public_html/html", cwd=doc_root)
        system_cmd("rsync -a --delete ${HOME}/repos/sknrf-core/doc/build/doctrees/ scikitno@scikit-nonlinear.org:/home/scikitno/public_html/doctrees", cwd=doc_root)


setup(
    version=VERSION,
    package_dir={'sknrf': 'sknrf'},
    include_package_data=True,
    packages=find_packages(exclude=['doc', 'tests*']),
    entry_points={
        'gui_scripts': ['main = sknrf.main:main'],
    },
    # Support functions
    cmdclass={
            # Clean
            'clean': clean,
            'clean_clib': clean_clib,
            'clean_py': clean_py,
            'clean_doc': clean_doc,
            # Configure
            'config': config,
            'config_clib': config_clib,
            # Build
            'build': build,
            'build_clib': build_clib,
            #'build_py': (Included),
            # Install
            'install': install,
            'install_clib': install_clib,
            'install_doc': install_doc,
            'install_data': install_data,
            # Distribute
            'bdist_wheel': bdist_wheel,
            # Upload
            'upload': upload,
            'upload_pypi': upload_pypi,
            'upload_doc': upload_doc}
)

