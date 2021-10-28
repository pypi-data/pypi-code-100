# -*- coding: utf-8 -*-
import os
import re
import subprocess
import sys

from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext

from setuptools.dist import Distribution
import shutil


def convert_to_none_any(name):
	current_index = 0
	target_index = 0
	counter = 0
	for char in name:
		if char == '-':
			counter += 1
		if counter == 3:
			target_index = current_index + 1
			break
		current_index += 1
	name = name[:target_index] + 'none-any.whl'
	return name




# Convert distutils Windows platform specifiers to CMake -A arguments
PLAT_TO_CMAKE = {
    "win32": "Win32",
    "win-amd64": "x64",
    "win-arm32": "ARM",
    "win-arm64": "ARM64",
}


# A CMakeExtension needs a sourcedir instead of a file list.
# The name must be the _single_ output extension from the CMake build.
# If you need multiple extensions, see scikit-build.
class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=""):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))

        # required for auto-detection & inclusion of auxiliary "native" libs
        if not extdir.endswith(os.path.sep):
            extdir += os.path.sep

        debug = int(os.environ.get("DEBUG", 0)) if self.debug is None else self.debug
        cfg = "Debug" if debug else "Release"

        # CMake lets you override the generator - we need to check this.
        # Can be set with Conda-Build, for example.
        cmake_generator = os.environ.get("CMAKE_GENERATOR", "")

        # Set Python_EXECUTABLE instead if you use PYBIND11_FINDPYTHON
        # EXAMPLE_VERSION_INFO shows you how to pass a value into the C++ code
        # from Python.
        cmake_args = [
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={}".format(extdir),
            "-DCMAKE_BUILD_TYPE={}".format(cfg),  # not used on MSVC, but no harm
        ]
        build_args = []
        # Adding CMake arguments set as environment variable
        # (needed e.g. to build for ARM OSx on conda-forge)
        if "CMAKE_ARGS" in os.environ:
            cmake_args += [item for item in os.environ["CMAKE_ARGS"].split(" ") if item]

        # In this example, we pass in the version to C++. You might not need to.
        cmake_args += [
            "-DEXAMPLE_VERSION_INFO={}".format(self.distribution.get_version())
        ]

        if self.compiler.compiler_type != "msvc":
            # Using Ninja-build since it a) is available as a wheel and b)
            # multithreads automatically. MSVC would require all variables be
            # exported for Ninja to pick it up, which is a little tricky to do.
            # Users can override the generator with CMAKE_GENERATOR in CMake
            # 3.15+.
            if not cmake_generator:
                try:
                    import ninja  # noqa: F401

                    cmake_args += ["-GNinja"]
                except ImportError:
                    pass

        else:

            # Single config generators are handled "normally"
            single_config = any(x in cmake_generator for x in {"NMake", "Ninja"})

            # CMake allows an arch-in-generator style for backward compatibility
            contains_arch = any(x in cmake_generator for x in {"ARM", "Win64"})

            # Specify the arch if using MSVC generator, but only if it doesn't
            # contain a backward-compatibility arch spec already in the
            # generator name.
            if not single_config and not contains_arch:
                cmake_args += ["-A", PLAT_TO_CMAKE[self.plat_name]]

            # Multi-config generators have a different way to specify configs
            if not single_config:
                cmake_args += [
                    "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}".format(cfg.upper(), extdir)
                ]
                build_args += ["--config", cfg]

        if sys.platform.startswith("darwin"):
            # Cross-compile support for macOS - respect ARCHFLAGS if set
            archs = re.findall(r"-arch (\S+)", os.environ.get("ARCHFLAGS", ""))
            # if archs:
            #     cmake_args += ["-DCMAKE_OSX_ARCHITECTURES={}".format(";".join(archs))]

            cmake_args += ["-DCMAKE_OSX_ARCHITECTURES=x86_64"]

        # Set CMAKE_BUILD_PARALLEL_LEVEL to control the parallel build level
        # across all generators.
        if "CMAKE_BUILD_PARALLEL_LEVEL" not in os.environ:
            # self.parallel is a Python 3 only way to set parallel jobs by hand
            # using -j in the build_ext call, not supported by pip or PyPA-build.
            if hasattr(self, "parallel") and self.parallel:
                # CMake 3.12+ only.
                build_args += ["-j{}".format(self.parallel)]

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        # print(ext.sourcedir)
        # print("####")
        # print(os.listdir())
        # print("####")
        subprocess.check_call(
            ["cmake", ext.sourcedir] + cmake_args, cwd=self.build_temp
        )
        subprocess.check_call(
            ["cmake", "--build", "."] + build_args, cwd=self.build_temp
        )

def renamer():
	pass


# The information here can also be placed in setup.cfg - better separation of
# logic and declaration, and simpler if you include description/version in a file.
setup_kwargs = dict(
    name="pysiclib",
    version="0.0.5",
    author="Shameek Conyers",
		author_email="sic@usf.edu",
    description="A General Scientific Computation Library",
    long_description="",
		url="https://ShameekConyers.com/siclib",
    ext_modules=[CMakeExtension("pysiclib._pysiclib")],
    cmdclass={"build_ext": CMakeBuild},
    zip_safe=False,
		packages=find_packages(),
    extras_require={"test": ["pytest"]},
		package_data={'': ['*', 'LICENSE'], "pysiclib": ["**/*.pyi", "**/*.py"]},
    install_requires=[],
)

set_result = setup(
	**setup_kwargs
)

try:
	wheel_built = 'dist/{}-{}.whl'\
		.format(set_result.command_obj['bdist_wheel'].wheel_dist_name,
			'-'.join(set_result.command_obj['bdist_wheel'].get_tag()))

	target_wheel = convert_to_none_any(wheel_built)
	try:
		shutil.copy(wheel_built, target_wheel)
		os.remove(wheel_built)
	except:
		dir_items = os.listdir('./dist')
		for item in dir_items:
			if "dist/" + item != target_wheel:
				shutil.copy("dist/" + item, target_wheel)
				os.remove("dist/" + item)
except:
	pass
