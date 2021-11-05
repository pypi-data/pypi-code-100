"""
Module containing most of the utility functions for the binarycpython package

Functions here are mostly functions used in other classes/functions, or
useful functions for the user

Tasks:
    - TODO: change all prints to verbose_prints
"""


import bz2
import collections
from colorama import Fore, Back, Style
import copy
import datetime as dt
import gc
import gzip
from halo import Halo
import h5py
import humanize
import inspect
from io import StringIO
import json
import msgpack
import numpy as np
import os
import psutil
import py_rinterpolate
import re
import resource
import sys
import subprocess
import tempfile
import time
import types
from typing import Union, Any

import simplejson

# import orjson

import astropy.units as u
import binarycpython.utils.moe_di_stefano_2017_data as moe_di_stefano_2017_data

from binarycpython import _binary_c_bindings
from binarycpython.utils.dicts import filter_dict, filter_dict_through_values


########################################################
# Unsorted
########################################################


def format_number(number):
    # compact number formatter

    string = "{number:.2g}".format(number=number)
    string = string.replace("e+0", "e+")
    string = string.replace("e-0", "e-")

    return string


def check_if_in_shell():
    """
    Function to check whether the script is running from a shell
    """

    if sys.stdin and sys.stdin.isatty():
        in_shell = True
    else:
        in_shell = False

    return in_shell


def timedelta(delta):
    """
    Function to convert a length of time (float, seconds) to a string for
    human-readable output.
    """
    # currently use the humanize module to do this
    t = humanize.time.precisedelta(
        dt.timedelta(seconds=delta),
        format="%0.2f",
        minimum_unit="milliseconds",
        suppress=["milliseconds"],
    )
    # and use more compact units
    t = t.replace(" days and", "d")
    t = t.replace(" hours and", "h")
    t = t.replace(" minutes and", "m")
    t = t.replace(" seconds and", "s")
    t = t.replace(" days", "d")
    t = t.replace(" hours", "h")
    t = t.replace(" minutes", "m")
    t = t.replace(" seconds", "s")
    return t


def get_ANSI_colours():
    # ANSI colours dictionary
    foreground_colours = {
        "red": Fore.RED,
        "yellow": Fore.YELLOW,
        "blue": Fore.BLUE,
        "cyan": Fore.CYAN,
        "green": Fore.GREEN,
        "magenta": Fore.MAGENTA,
        "white": Fore.WHITE,
        "black": Fore.BLACK,
    }

    background_colours = {
        "red": Back.RED,
        "yellow": Back.YELLOW,
        "blue": Back.BLUE,
        "cyan": Back.CYAN,
        "green": Back.GREEN,
        "magenta": Back.MAGENTA,
        "white": Back.WHITE,
        "black": Back.BLACK,
    }

    default_style = Style.BRIGHT
    colours = {}

    for c in foreground_colours:
        colours[c] = default_style + foreground_colours[c]
        for d in background_colours:
            colours[c + " on " + d] = foreground_colours[c] + background_colours[d]
    colours["reset"] = Style.RESET_ALL

    return colours


def mem_use():
    """
    Return current process memory use in MB. (Takes no arguments) Note: this is per-thread only.
    """

    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def trem(dt, count, dn, n):
    """
    Estimate time remaining (seconds) given a differential time and count (i.e. progress = $count/$n). $dt is the time since the last call, $count is the current progress count, $dn is the number run since the last call, and $n is the total number required.
    """
    tpr = dt / max(1, dn)
    etasecs = tpr * (n - count)
    (eta, units) = conv_time_units(etasecs)
    return (eta, units, tpr, etasecs)


def conv_time_units(t):
    """
    Converts time (t, in seconds, passing in as the only argument) to seconds, minutes or hours depending on its magnitude. Returns a tuple (t,units).
    """
    units = "s"
    # default to seconds
    if t > 60:
        t /= 60
        units = "m"
    if t > 60:
        t /= 60
        units = "h"
    return (t, units)


def bin_data(value, binwidth):
    """
    Function that bins the data

    Uses the absolute value of binwidth
    """

    return ((0.5 if value > 0.0 else -0.5) + int(value / abs(binwidth))) * abs(binwidth)


def convert_bytes(size):
    """
    Function to return the size + a magnitude string
    """

    for name in ["bytes", "KB", "MB", "GB", "TB"]:
        if size < 1024.0:
            return "%3.1f %s" % (size, name)
        size /= 1024.0

    return size


def get_size(obj, seen=None):
    """
    Recursively finds size of objects

    From https://github.com/bosswissam/pysize
    """

    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, "__dict__"):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, "__iter__") and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size


def get_moe_di_stefano_dataset(options, verbosity=0):
    """
    Function to get the default Moe and di Stefano dataset or accept a user input.

    Returns a dict containing the (JSON) data.
    """

    json_data = None

    if "JSON" in options:
        # use the JSON data passed in
        json_data = options["JSON"]

    elif "file" in options:
        # use the file passed in, if provided
        if not os.path.isfile(options["file"]):
            verbose_print(
                "The provided 'file' Moe and de Stefano JSON file does not seem to exist at {}".format(
                    options["file"]
                ),
                verbosity,
                1,
            )

            raise ValueError
        if not options["file"].endswith(".json"):
            verbose_print(
                "Provided filename is not a json file",
                verbosity,
                1,
            )

        else:
            # Read input data and Clean up the data if there are white spaces around the keys
            with open(options["file"], "r") as data_filehandle:
                datafile_data = data_filehandle.read()
                datafile_data = datafile_data.replace('" ', '"')
                datafile_data = datafile_data.replace(' "', '"')
                datafile_data = datafile_data.replace(' "', '"')
                json_data = json.loads(datafile_data)

    if not json_data:
        # no JSON data or filename given, use the default 2017 dataset
        verbose_print(
            "Using the default Moe and de Stefano 2017 datafile",
            verbosity,
            1,
        )
        json_data = copy.deepcopy(moe_di_stefano_2017_data.moe_di_stefano_2017_data)

    return json_data


def imports():
    for name, val in globals().items():
        if isinstance(val, types.ModuleType):
            yield val.__name__


def convfloat(x):
    """
    Convert scalar x to a float if we can, in which case return the float, otherwise just return x without changing it. Usually, x is a string, but could be anything that float() can handle without failure.
    """
    try:
        y = float(x)
        return y
    except ValueError:
        return x


def datalinedict(line: str, parameters: list):
    """
    Convert a line of data to a more convenient dictionary.
    Arguments:
       line = a line of data as a string
       parameters = a list of the parameter names

    Note: if the parameter is a floating point number, it will be converted to Python's float type.
    """

    return {param: convfloat(value) for param, value in zip(parameters, line.split())}


def pad_output_distribution(dist: dict, binwidth: float):
    """
    Given a distribution, dist (a dictionary), which should be binned every binwidth (float), fill the distribution with zeros when there is no data. Note: this changes the data in place.
    """

    # sorted list of the keys
    skeys = sorted(dist.keys(), key=lambda x: float(x))

    # get min and max, offset by the binwidth
    min_val = skeys[0] - binwidth
    max_val = skeys[-1] + binwidth

    # pad with zeros
    x = min_val
    while x <= max_val:
        dist[x] = dist.setdefault(x, 0.0)
        x += binwidth

    return dist


class catchtime(object):
    """
    Context manager to calculate time spent
    """

    def __enter__(self):
        """On entry we start the clock"""
        self.t = time.clock()
        return self

    def __exit__(self, type, value, traceback):
        """On exit we stop the clock and measure the time spent"""
        self.t = time.clock() - self.t
        print("Took {}s".format(self.t))


def is_capsule(o):
    """
    Function to tell whether object is a capsule
    """

    t = type(o)
    return t.__module__ == "builtins" and t.__name__ == "PyCapsule"


class Capturing(list):
    """
    Context manager to capture output and store it
    """

    def __enter__(self):
        """On entry we capture the stdout output"""

        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        """On exit we release the capture again"""

        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio  # free up some memory
        sys.stdout = self._stdout


def call_binary_c_config(argument):
    """
    Function to interface with the binary_c config file

    input:
        - argument: argument for the binary_c config

    Returns:
        - raw output of binary_c-config
    """

    BINARY_C_DIR = os.getenv("BINARY_C", None)
    if not BINARY_C_DIR:
        msg = "Error: the BINARY_C environment variable is not set. Aborting"
        raise ValueError(msg)

    BINARY_C_CONFIG = os.path.join(BINARY_C_DIR, "binary_c-config")
    if not os.path.isfile(BINARY_C_CONFIG):
        msg = "binary_c-config file does not exist. Aborting"
        raise ValueError(msg)

    output = subprocess.run(
        [BINARY_C_CONFIG, argument], stdout=subprocess.PIPE, check=True
    ).stdout.decode("utf-8")

    return output


########################################################
# utility functions
########################################################


def verbose_print(message: str, verbosity: int, minimal_verbosity: int) -> None:
    """
    Function that decides whether to print a message based on the current verbosity
    and its minimum verbosity

    if verbosity is equal or higher than the minimum, then we print

    Args:
        message: message to print
        verbosity: current verbosity level
        minimal_verbosity: threshold verbosity above which to print
    """

    if verbosity >= minimal_verbosity:
        print(message)
        sys.stdout.flush()


def remove_file(file: str, verbosity: int = 0) -> None:
    """
    Function to remove files but with verbosity

    Args:
        file: full file path to the file that will be removed.
        verbosity: current verbosity level (Optional)

    Returns:
        the path of a sub directory called binary_c_python in the TMP of the file system

    """

    if os.path.exists(file):
        if not os.path.isfile(file):
            verbose_print(
                "This path ({}) is a directory, not a file".format(file), verbosity, 0
            )

        try:
            verbose_print("Removed {}".format(file), verbosity, 1)
            os.remove(file)

        except FileNotFoundError as inst:
            print("Error while deleting file {}: {}".format(file, inst))
    else:
        verbose_print(
            "File/directory {} doesn't exist. Can't remove it.".format(file),
            verbosity,
            1,
        )


def get_username():
    return psutil.Process().username()


def temp_dir(*args: str) -> str:
    """
    Function to create directory within the TMP directory of the file system

    Makes use of os.makedirs exist_ok which requires python 3.2+

    Args:
        function arguments: str input where each next input will be a child of the previous full_path. e.g. temp_dir('tests', 'grid') will become '/tmp/binary_c_python/tests/grid'

    Returns:
        the path of a sub directory called binary_c_python in the TMP of the file system
    """

    tmp_dir = tempfile.gettempdir()
    username = get_username()
    path = os.path.join(tmp_dir, "binary_c_python-{}".format(username))

    # loop over the other paths if there are any:
    if args:
        for extra_dir in args:
            path = os.path.join(path, extra_dir)

    #
    os.makedirs(path, exist_ok=True)

    return path


def create_hdf5(data_dir: str, name: str) -> None:
    """
    Function to create an hdf5 file from the contents of a directory:
     - settings file is selected by checking on files ending on settings
     - data files are selected by checking on files ending with .dat

    TODO: fix missing settings files

    Args:
        data_dir: directory containing the data files and settings file
        name: name of hdf5file.

    """

    # Make HDF5:
    # Create the file
    hdf5_filename = os.path.join(data_dir, "{}".format(name))
    print("Creating {}".format(hdf5_filename))
    hdf5_file = h5py.File(hdf5_filename, "w")

    # Get content of data_dir
    content_data_dir = os.listdir(data_dir)

    # Settings
    if any([file.endswith("_settings.json") for file in content_data_dir]):
        print("Adding settings to HDF5 file")
        settings_file = os.path.join(
            data_dir,
            [file for file in content_data_dir if file.endswith("_settings.json")][0],
        )

        with open(settings_file, "r") as settings_file:
            settings_json = json.load(settings_file)

        # Create settings group
        settings_grp = hdf5_file.create_group("settings")

        # Write version_string to settings_group
        settings_grp.create_dataset("used_settings", data=json.dumps(settings_json))

    # Get data files
    data_files = [el for el in content_data_dir if el.endswith(".dat")]
    if data_files:
        print("Adding data to HDF5 file")

        # Create the data group
        data_grp = hdf5_file.create_group("data")

        # Write the data to the file:
        # Make sure:
        for data_file in data_files:
            # filename stuff
            filename = data_file
            full_path = os.path.join(data_dir, filename)
            base_name = os.path.splitext(os.path.basename(filename))[0]

            # Get header info
            header_name = "{base_name}_header".format(base_name=base_name)
            data_headers = np.genfromtxt(full_path, dtype="str", max_rows=1)
            data_headers = np.char.encode(data_headers)
            data_grp.create_dataset(header_name, data=data_headers)

            # Add data
            data = np.loadtxt(full_path, skiprows=1)
            data_grp.create_dataset(base_name, data=data)

        hdf5_file.close()


########################################################
# version_info functions
########################################################


def return_binary_c_version_info(parsed: bool = True) -> Union[str, dict]:
    """
    Function that returns the version information of binary_c. This function calls the function
    _binary_c_bindings.return_version_info()

    Args:
        parsed: Boolean flag whether to parse the version_info output of binary_c. default = False

    Returns:
        Either the raw string of binary_c or a parsed version of this in the form of a nested
        dictionary
    """

    found_prev = False
    if "BINARY_C_MACRO_HEADER" in os.environ:
        # the env var is already present. lets save that and put that back later
        found_prev = True
        prev_value = os.environ["BINARY_C_MACRO_HEADER"]

    #
    os.environ["BINARY_C_MACRO_HEADER"] = "macroxyz"

    # Get version_info
    version_info = _binary_c_bindings.return_version_info().strip()

    # parse if wanted
    if parsed:
        version_info = parse_binary_c_version_info(version_info)

    # delete value
    del os.environ["BINARY_C_MACRO_HEADER"]

    # put stuff back if we found a previous one
    if found_prev:
        os.environ["BINARY_C_MACRO_HEADER"] = prev_value

    return version_info


def parse_binary_c_version_info(version_info_string: str) -> dict:
    """
    Function that parses the binary_c version info. Long function with a lot of branches

    TODO: fix this function. stuff is missing: isotopes, macros, nucleosynthesis_sources

    Args:
        version_info_string: raw output of version_info call to binary_c

    Returns:
        Parsed version of the version info, which is a dictionary containing the keys: 'isotopes' for isotope info, 'argpairs' for argument pair info (TODO: explain), 'ensembles' for ensemble settings/info, 'macros' for macros, 'elements' for atomic element info, 'DTlimit' for (TODO: explain), 'nucleosynthesis_sources' for nucleosynthesis sources, and 'miscellaneous' for all those that were not caught by the previous groups. 'git_branch', 'git_build', 'revision' and 'email' are also keys, but its clear what those contain.
    """

    version_info_dict = {}

    # Clean data and put in correct shape
    splitted = version_info_string.strip().splitlines()
    cleaned = {el.strip() for el in splitted if not el == ""}

    ##########################
    # Network:
    # Split off all the networks and parse the info.

    networks = {el for el in cleaned if el.startswith("Network ")}
    cleaned = cleaned - networks

    networks_dict = {}
    for el in networks:
        network_dict = {}
        split_info = el.split("Network ")[-1].strip().split("==")

        network_number = int(split_info[0])
        network_dict["network_number"] = network_number

        network_info_split = split_info[1].split(" is ")

        shortname = network_info_split[0].strip()
        network_dict["shortname"] = shortname

        if not network_info_split[1].strip().startswith(":"):
            network_split_info_extra = network_info_split[1].strip().split(":")

            longname = network_split_info_extra[0].strip()
            network_dict["longname"] = longname

            implementation = (
                network_split_info_extra[1].strip().replace("implemented in", "")
            )
            if implementation:
                network_dict["implemented_in"] = implementation.strip().split()

        networks_dict[network_number] = copy.deepcopy(network_dict)
    version_info_dict["networks"] = networks_dict if networks_dict else None

    ##########################
    # Isotopes:
    # Split off
    isotopes = {el for el in cleaned if el.startswith("Isotope ")}
    cleaned = cleaned - isotopes

    isotope_dict = {}
    for el in isotopes:
        split_info = el.split("Isotope ")[-1].strip().split(" is ")

        isotope_info = split_info[-1]
        name = isotope_info.split(" ")[0].strip()

        # Get details
        mass_g = float(
            isotope_info.split(",")[0].split("(")[1].split("=")[-1][:-2].strip()
        )
        mass_amu = float(
            isotope_info.split(",")[0].split("(")[-1].split("=")[-1].strip()
        )
        mass_mev = float(
            isotope_info.split(",")[-3].split("=")[-1].replace(")", "").strip()
        )
        A = int(isotope_info.split(",")[-1].strip().split("=")[-1].replace(")", ""))
        Z = int(isotope_info.split(",")[-2].strip().split("=")[-1])

        #
        isotope_dict[int(split_info[0])] = {
            "name": name,
            "Z": Z,
            "A": A,
            "mass_mev": mass_mev,
            "mass_g": mass_g,
            "mass_amu": mass_amu,
        }
    version_info_dict["isotopes"] = isotope_dict if isotope_dict else None

    ##########################
    # Arg pairs:
    # Split off
    argpairs = set([el for el in cleaned if el.startswith("ArgPair")])
    cleaned = cleaned - argpairs

    argpair_dict = {}
    for el in sorted(argpairs):
        split_info = el.split("ArgPair ")[-1].split(" ")

        if not argpair_dict.get(split_info[0], None):
            argpair_dict[split_info[0]] = {split_info[1]: split_info[2]}
        else:
            argpair_dict[split_info[0]][split_info[1]] = split_info[2]

    version_info_dict["argpairs"] = argpair_dict if argpair_dict else None

    ##########################
    # ensembles:
    # Split off
    ensembles = {el for el in cleaned if el.startswith("Ensemble")}
    cleaned = cleaned - ensembles

    ensemble_dict = {}
    ensemble_filter_dict = {}
    for el in ensembles:
        split_info = el.split("Ensemble ")[-1].split(" is ")

        if len(split_info) > 1:
            if not split_info[0].startswith("filter"):
                ensemble_dict[int(split_info[0])] = split_info[-1]
            else:
                filter_no = int(split_info[0].replace("filter ", ""))
                ensemble_filter_dict[filter_no] = split_info[-1]

    version_info_dict["ensembles"] = ensemble_dict if ensemble_dict else None
    version_info_dict["ensemble_filters"] = (
        ensemble_filter_dict if ensemble_filter_dict else None
    )

    ##########################
    # macros:
    # Split off
    macros = {el for el in cleaned if el.startswith("macroxyz")}
    cleaned = cleaned - macros

    param_type_dict = {
        "STRING": str,
        "FLOAT": float,
        "MACRO": str,
        "INT": int,
        "LONG_INT": int,
        "UINT": int,
    }

    macros_dict = {}
    for el in macros:
        split_info = el.split("macroxyz ")[-1].split(" : ")
        param_type = split_info[0]

        new_split = "".join(split_info[1:]).split(" is ")
        param_name = new_split[0]
        param_value = " is ".join(new_split[1:])

        # Sometimes the macros have extra information behind it. Needs an update in outputting by binary_c
        try:
            macros_dict[param_name] = param_type_dict[param_type](param_value)
        except ValueError:
            macros_dict[param_name] = str(param_value)
    version_info_dict["macros"] = macros_dict if macros_dict else None

    ##########################
    # Elements:
    # Split off:
    elements = {el for el in cleaned if el.startswith("Element")}
    cleaned = cleaned - elements

    # Fill dict:
    elements_dict = {}
    for el in elements:
        split_info = el.split("Element ")[-1].split(" : ")
        name_info = split_info[0].split(" is ")

        # get isotope info
        isotopes = {}
        if not split_info[-1][0] == "0":
            isotope_string = split_info[-1].split(" = ")[-1]
            isotopes = {
                int(split_isotope.split("=")[0]): split_isotope.split("=")[1]
                for split_isotope in isotope_string.split(" ")
            }

        elements_dict[int(name_info[0])] = {
            "name": name_info[-1],
            "atomic_number": int(name_info[0]),
            "amt_isotopes": len(isotopes),
            "isotopes": isotopes,
        }
    version_info_dict["elements"] = elements_dict if elements_dict else None

    ##########################
    # dt_limits:
    # split off
    dt_limits = {el for el in cleaned if el.startswith("DTlimit")}
    cleaned = cleaned - dt_limits

    # Fill dict
    dt_limits_dict = {}
    for el in dt_limits:
        split_info = el.split("DTlimit ")[-1].split(" : ")
        dt_limits_dict[split_info[1].strip()] = {
            "index": int(split_info[0]),
            "value": float(split_info[-1]),
        }

    version_info_dict["dt_limits"] = dt_limits_dict if dt_limits_dict else None

    ##########################
    # Nucleosynthesis sources:
    # Split off
    nucsyn_sources = {el for el in cleaned if el.startswith("Nucleosynthesis")}
    cleaned = cleaned - nucsyn_sources

    # Fill dict
    nucsyn_sources_dict = {}
    for el in nucsyn_sources:
        split_info = el.split("Nucleosynthesis source")[-1].strip().split(" is ")
        nucsyn_sources_dict[int(split_info[0])] = split_info[-1]

    version_info_dict["nucleosynthesis_sources"] = (
        nucsyn_sources_dict if nucsyn_sources_dict else None
    )

    ##########################
    # miscellaneous:
    # All those that I didn't catch with the above filters. Could try to get some more out though.
    # TODO: filter a bit more.

    misc_dict = {}

    # Filter out git revision
    git_revision = [el for el in cleaned if el.startswith("git revision")]
    misc_dict["git_revision"] = (
        git_revision[0].split("git revision ")[-1].replace('"', "")
    )
    cleaned = cleaned - set(git_revision)

    # filter out git url
    git_url = [el for el in cleaned if el.startswith("git URL")]
    misc_dict["git_url"] = git_url[0].split("git URL ")[-1].replace('"', "")
    cleaned = cleaned - set(git_url)

    # filter out version
    version = [el for el in cleaned if el.startswith("Version")]
    misc_dict["version"] = str(version[0].split("Version ")[-1])
    cleaned = cleaned - set(version)

    git_branch = [el for el in cleaned if el.startswith("git branch")]
    misc_dict["git_branch"] = git_branch[0].split("git branch ")[-1].replace('"', "")
    cleaned = cleaned - set(git_branch)

    build = [el for el in cleaned if el.startswith("Build")]
    misc_dict["build"] = build[0].split("Build: ")[-1].replace('"', "")
    cleaned = cleaned - set(build)

    email = [el for el in cleaned if el.startswith("Email")]
    misc_dict["email"] = email[0].split("Email ")[-1].split(",")
    cleaned = cleaned - set(email)

    other_items = set([el for el in cleaned if " is " in el])
    cleaned = cleaned - other_items

    for el in other_items:
        split = el.split(" is ")
        key = split[0].strip()
        val = " is ".join(split[1:]).strip()
        misc_dict[key] = val

    misc_dict["uncaught"] = list(cleaned)

    version_info_dict["miscellaneous"] = misc_dict if misc_dict else None
    return version_info_dict


########################################################
# binary_c output functions
########################################################


def output_lines(output: str) -> list:
    """
    Function that outputs the lines that were received from the binary_c run, but now as an iterator.

    Args:
        output: raw binary_c output

    Returns:
        Iterator over the lines of the binary_c output
    """

    if output:
        return output.splitlines()
    return []


def example_parse_output(output: str, selected_header: str) -> dict:
    """
    Function that parses output of binary_c. This version serves as an example and is quite
    detailed. Custom functions can be easier:

    This function works in two cases:
    if the caught line contains output like 'example_header time=12.32 mass=0.94 ..'
    or if the line contains output like 'example_header 12.32 0.94'
    Please don't the two cases.

    You can give a 'selected_header' to catch any line that starts with that.
    Then the values will be put into a dictionary.

    Tasks:
        - TODO: Think about exporting to numpy array or pandas instead of a defaultdict
        - TODO: rethink whether this function is necessary at all
        - TODO: check this function again

    Args:
        output: binary_c output string
        selected_header: string header of the output (the start of the line that you want to
            process)

    Returns:
        dictionary containing parameters as keys and lists for the values
    """

    value_dicts = []

    # split output on newlines
    for line in output.split("\n"):
        # Skip any blank lines
        if not line == "":
            split_line = line.split()

            # Select parts
            header = split_line[0]
            values_list = split_line[1:]

            # print(values_list)
            # Catch line starting with selected header
            if header == selected_header:
                # Check if the line contains '=' symbols:
                value_dict = {}
                if all("=" in value for value in values_list):
                    for value in values_list:
                        key, val = value.split("=")
                        value_dict[key.strip()] = val.strip()
                    value_dicts.append(value_dict)
                else:
                    if any("=" in value for value in values_list):
                        raise ValueError(
                            "Caught line contains some = symbols but not \
                            all of them do. aborting run"
                        )

                    for j, val in enumerate(values_list):
                        value_dict[j] = val
                    value_dicts.append(value_dict)

    if len(value_dicts) == 0:
        print(
            "Sorry, didn't find any line matching your header {}".format(
                selected_header
            )
        )
        return None

    keys = value_dicts[0].keys()

    # Construct final dict.
    final_values_dict = collections.defaultdict(list)
    for value_dict in value_dicts:
        for key in keys:
            final_values_dict[key].append(value_dict[key])

    return final_values_dict


########################################################
# Argument and default value functions
########################################################


def get_defaults(filter_values: bool = False) -> dict:
    """
    Function that calls the binaryc get args function and cast it into a dictionary.

    All the values are strings

    Args:
        filter_values: whether to filter out NULL and Function defaults.

    Returns:
        dictionary containing the parameter name as key and the parameter default as value
    """

    default_output = _binary_c_bindings.return_arglines()
    default_dict = {}

    for default in default_output.split("\n"):
        if not default in ["__ARG_BEGIN", "__ARG_END", ""]:
            key, value = default.split(" = ")
            default_dict[key] = value

    if filter_values:
        default_dict = filter_arg_dict(default_dict)

    return default_dict


def get_arg_keys() -> list:
    """
    Function that return the list of possible keys to give in the arg string.
    This function calls get_defaults()

    Returns:
        list of all the parameters that binary_c accepts (and has default values for, since
        we call get_defaults())
    """

    return list(get_defaults().keys())


def filter_arg_dict(arg_dict: dict) -> dict:
    """
    Function to filter out keys that contain values included in ['NULL', 'Function', '']

    This function is called by get_defaults()

    Args:
        arg_dict: dictionary containing the argument + default key pairs of binary_c

    Returns:
        filtered dictionary (pairs with NULL and Function values are removed)
    """

    return filter_dict_through_values(arg_dict.copy(), ["NULL", "Function", ""])


def create_arg_string(
    arg_dict: dict, sort: bool = False, filter_values: bool = False
) -> str:
    """
    Function that creates the arg string for binary_c. Takes a dictionary containing the arguments
    and writes them to a string
    This string is missing the 'binary_c ' at the start.

    Args:
        arg_dict: dictionary
        sort: (optional, default = False) Boolean whether to sort the order of the keys.
        filter_values: (optional, default = False) filters the input dict on keys that have NULL or `function` as value.

    Returns:
        The string built up by combining all the key + value's.
    """

    arg_string = ""

    # Whether to filter the arguments
    if filter_values:
        arg_dict = filter_arg_dict(arg_dict)

    #
    keys = sorted(arg_dict.keys()) if sort else arg_dict.keys()

    #
    for key in keys:
        arg_string += "{key} {value} ".format(key=key, value=arg_dict[key])

    arg_string = arg_string.strip()
    return arg_string


########################################################
# Help functions
########################################################


def get_help(
    param_name: str = "", print_help: bool = True, fail_silently: bool = False
) -> Union[dict, None]:
    """
    Function that returns the help info for a given parameter, by interfacing with binary_c

    Will check whether it is a valid parameter.

    Binary_c will output things in the following order;
    - Did you mean?
    - binary_c help for variable
    - default
    - available macros

    This function reads out that structure and catches the different components of this output

    Tasks:
        - TODO: consider not returning None, but return empty dict

    Args:
        param_name: name of the parameter that you want info from. Will get checked whether its a
            valid parameter name
        print_help: (optional, default = True) whether to print out the help information
        fail_silently: (optional, default = False) Whether to print the errors raised if the
        parameter isn't valid

    Returns:
        Dictionary containing the help info. This dictionary contains 'parameter_name',
        'parameter_value_input_type', 'description', optionally 'macros'
    """

    available_arg_keys = get_arg_keys()

    if not param_name:
        print(
            "Please set the param_name to any of the following:\n {}".format(
                sorted(available_arg_keys)
            )
        )
        return None

    if param_name in available_arg_keys:
        help_info = _binary_c_bindings.return_help(param_name)
        cleaned = [el for el in help_info.split("\n") if not el == ""]

        # Get line numbers
        did_you_mean_nr = [
            i for i, el in enumerate(cleaned) if el.startswith("Did you mean")
        ]
        parameter_line_nr = [
            i for i, el in enumerate(cleaned) if el.startswith("binary_c help")
        ]
        default_line_nr = [
            i for i, el in enumerate(cleaned) if el.startswith("Default")
        ]
        macros_line_nr = [
            i for i, el in enumerate(cleaned) if el.startswith("Available")
        ]

        help_info_dict = {}

        # Get alternatives
        if did_you_mean_nr:
            alternatives = cleaned[did_you_mean_nr[0] + 1 : parameter_line_nr[0]]
            alternatives = [el.strip() for el in alternatives]
            help_info_dict["alternatives"] = alternatives

        # Information about the parameter
        parameter_line = cleaned[parameter_line_nr[0]]
        parameter_name = parameter_line.split(":")[1].strip().split(" ")[0]
        parameter_value_input_type = (
            " ".join(parameter_line.split(":")[1].strip().split(" ")[1:])
            .replace("<", "")
            .replace(">", "")
        )

        help_info_dict["parameter_name"] = parameter_name
        help_info_dict["parameter_value_input_type"] = parameter_value_input_type

        description_line = " ".join(
            cleaned[parameter_line_nr[0] + 1 : default_line_nr[0]]
        )
        help_info_dict["description"] = description_line

        # Default:
        default_line = cleaned[default_line_nr[0]]
        default_value = default_line.split(":")[-1].strip()

        help_info_dict["default"] = default_value

        # Get Macros:
        if macros_line_nr:
            macros = cleaned[macros_line_nr[0] + 1 :]
            help_info_dict["macros"] = macros

        if print_help:
            for key in help_info_dict:
                print("{}:\n\t{}".format(key, help_info_dict[key]))

        return help_info_dict

    else:
        if not fail_silently:
            print(
                "{} is not a valid parameter name. Please choose from the \
                following parameters:\n\t{}".format(
                    param_name, list(available_arg_keys)
                )
            )
        return None


def get_help_all(print_help: bool = True) -> dict:
    """
    Function that reads out the output of the return_help_all API call to binary_c. This return_help_all binary_c returns all the information for the parameters, their descriptions and other properties. The output is categorised in sections.

    Args:
        print_help: (optional, default = True) prints all the parameters and their descriptions.

    Returns:
        returns a dictionary containing dictionaries per section. These dictionaries contain the parameters and descriptions etc for all the parameters in that section
    """

    # Call function
    help_all = _binary_c_bindings.return_help_all()

    # String manipulation
    split = help_all.split(
        "############################################################\n"
    )
    cleaned = [el for el in split if not el == "\n"]

    section_nums = [i for i in range(len(cleaned)) if cleaned[i].startswith("#####")]

    # Create dicts
    help_all_dict = {}

    # Select the section name and the contents of that section. Note, not all sections have content!
    for i in range(len(section_nums)):
        if not i == len(section_nums) - 1:
            params = cleaned[section_nums[i] + 1 : section_nums[i + 1]]
        else:
            params = cleaned[section_nums[i] + 1 : len(cleaned)]
        section_name = (
            cleaned[section_nums[i]]
            .lstrip("#####")
            .strip()
            .replace("Section ", "")
            .lower()
        )

        #
        params_dict = {}

        if params:

            # Clean it, replace in-text newlines with a space and then split on newlines.
            split_params = params[0].strip().replace("\n ", " ").split("\n")

            # Process params and descriptions per section
            for split_param in split_params:
                split_param_info = split_param.split(" : ")
                if not len(split_param_info) == 3:
                    # there are occasions where the semicolon
                    # is used in the description text itself.
                    if len(split_param_info) == 4:
                        split_param_info = [
                            split_param_info[0],
                            ": ".join([split_param_info[1], split_param_info[2]]),
                            split_param_info[3],
                        ]

                    # other occasions?

                # Put the information in a dict
                param_name = split_param_info[0]
                param_description = split_param_info[1]

                if len(split_param_info) > 2:
                    rest = split_param_info[2:]
                else:
                    rest = None

                params_dict[param_name] = {
                    "param_name": param_name,
                    "description": param_description,
                    "rest": "".join(rest) if rest else "",
                }

            # make section_dict
            section_dict = {
                "section_name": section_name,
                "parameters": params_dict.copy(),
            }

            # Put in the total dict
            help_all_dict[section_name] = section_dict.copy()

    # Print things
    if print_help:
        for section in sorted(help_all_dict.keys()):
            print(
                "##################\n###### Section {}\n##################".format(
                    section
                )
            )
            section_dict = help_all_dict[section]
            for param_name in sorted(section_dict["parameters"].keys()):
                param = section_dict["parameters"][param_name]
                print(
                    "\n{}:\n\t{}: {}".format(
                        param["param_name"], param["description"], param["rest"]
                    )
                )

    # # Loop over all the parameters an call the help() function on it.
    # # Takes a long time but this is for testing
    # for section in help_all_dict.keys():
    #     section_dict = help_all_dict[section]
    #     for param in section_dict['parameters'].keys():
    #         get_help(param)

    return help_all_dict


def get_help_super(print_help: bool = False, fail_silently: bool = True) -> dict:
    """
    Function that first runs get_help_all, and then per argument also run
    the help function to get as much information as possible.

    Args:
        print_help: (optional, default = False) Whether to print the information
        fail_silently: (optional, default = True) Whether to fail silently or to print the errors

    Returns:
        dictionary containing all dictionaries per section, which then contain as much info as possible per parameter.
    """

    # Get help_all information
    help_all_dict = get_help_all(print_help=False)
    for section_name in help_all_dict:
        section = help_all_dict[section_name]

        # print(section_name)
        # for parameter_name in section["parameters"].keys():
        #     print("\t", parameter_name)

    help_all_super_dict = help_all_dict.copy()

    # Loop over all sections and stuff
    for section_name in help_all_dict:
        # Skipping the section i/o because that one shouldn't be available to python anyway
        if not section_name == "i/o":
            section = help_all_dict[section_name]

            for parameter_name in section["parameters"].keys():
                parameter = section["parameters"][parameter_name]

                # Get detailed help info
                detailed_help = get_help(
                    parameter_name,
                    print_help=False,
                    fail_silently=fail_silently,
                )

                if detailed_help:
                    # check whether the descriptions of help_all and detailed help are the same
                    if not fail_silently:
                        if not parameter["description"] == detailed_help["description"]:
                            print(json.dumps(parameter, indent=4))

                    ## put values into help all super dict
                    # input type
                    parameter["parameter_value_input_type"] = detailed_help[
                        "parameter_value_input_type"
                    ]

                    # default
                    parameter["default"] = detailed_help["default"]

                    # macros
                    if "macros" in detailed_help.keys():
                        parameter["macros"] = detailed_help["macros"]

                section["parameters"][parameter_name] = parameter

    if print_help:
        print(json.dumps(help_all_super_dict, indent=4))

    return help_all_super_dict


def make_build_text() -> str:
    """
    Function to make build text

    Returns:
        string containing information about the build and the git branch
    """

    version_info = return_binary_c_version_info(parsed=True)

    git_revision = version_info["miscellaneous"]["git_revision"]
    git_branch = version_info["miscellaneous"]["git_branch"]
    build_datetime = version_info["miscellaneous"]["build"]

    info_string = """
This information was obtained by the following binary_c build:
\t**binary_c git branch**: {}\t**binary_c git revision**: {}\t**Built on**: {}
""".format(
        git_branch, git_revision, build_datetime
    )

    return info_string.strip()


def write_binary_c_parameter_descriptions_to_rst_file(output_file: str) -> None:
    """
    Function that calls the get_help_super() to get the help text/descriptions for all the
    parameters available in that build.
    Writes the results to a .rst file that can be included in the docs.

    Tasks:
        - TODO: add the specific version git branch, git build, git commit, and binary_c version to
            this document

    Args:
        output_file: name of the output .rst file containing the ReStructuredText formatted output
            of all the binary_c parameters.
    """

    # Get the whole arguments dictionary
    arguments_dict = get_help_super()

    build_info = make_build_text()

    if not output_file.endswith(".rst"):
        print("Filename doesn't end with .rst, please provide a proper filename")
        return None

    with open(output_file, "w") as f:

        print("Binary\\_c parameters", file=f)
        print("{}".format("=" * len("Binary\\_c parameters")), file=f)
        print(
            "The following chapter contains all the parameters that the current version of binary\\_c can handle, along with their descriptions and other properties.",
            file=f,
        )
        print("\n", file=f)
        print(build_info, file=f)
        print("\n", file=f)

        for el in arguments_dict.keys():
            print("Section: {}".format(el), file=f)
            print("{}\n".format("-" * len("Section: {}".format(el))), file=f)
            # print(arguments_dict[el]['parameters'].keys())

            for arg in arguments_dict[el]["parameters"].keys():
                argdict = arguments_dict[el]["parameters"][arg]

                print("| **Parameter**: {}".format(argdict["param_name"]), file=f)
                print("| **Description**: {}".format(argdict["description"]), file=f)
                if "parameter_value_input_type" in argdict:
                    print(
                        "| **Parameter input type**: {}".format(
                            argdict["parameter_value_input_type"]
                        ),
                        file=f,
                    )
                if "default" in argdict:
                    print("| **Default value**: {}".format(argdict["default"]), file=f)
                if "macros" in argdict:
                    print("| **Macros**: {}".format(argdict["macros"]), file=f)
                if not argdict["rest"] == "(null)":
                    print("| **Extra**: {}".format(argdict["rest"]), file=f)
                print("", file=f)


########################################################
# log file functions
########################################################


def load_logfile(logfile: str) -> None:
    """
    Experimental function that parses the generated log file of binary_c.

    This function is not finished and shouldn't be used yet.

    Tasks:
        - TODO:

    Args:
        - logfile: filename of the log file you want to parse

    Returns:

    """

    with open(logfile, "r") as file:
        logfile_data = file.readlines()

    time_list = []
    m1_list = []
    m2_list = []
    k1_list = []
    k2_list = []
    sep_list = []
    ecc_list = []
    rel_r1_list = []
    rel_r2_list = []
    event_list = []

    # random_seed = logfile_data[0].split()[-2]
    # random_count = logfile_data[0].split()[-1]
    # probability = logfile_data[-1].split()

    for line in logfile_data[1:-1]:
        split_line = line.split()

        time_list.append(split_line[0])
        m1_list.append(split_line[1])
        m2_list.append(split_line[2])
        k1_list.append(split_line[3])
        k2_list.append(split_line[4])
        sep_list.append(split_line[5])
        ecc_list.append(split_line[6])
        rel_r1_list.append(split_line[7])
        rel_r2_list.append(split_line[8])
        event_list.append(" ".join(split_line[9:]))

    print(event_list)
