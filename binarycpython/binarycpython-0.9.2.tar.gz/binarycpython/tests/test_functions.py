"""
Unittests for the functions module
"""

import os
import unittest
import tempfile

import json
import h5py

from binarycpython.utils.custom_logging_functions import binary_c_log_code
from binarycpython.utils.run_system_wrapper import run_system
from binarycpython.utils.functions import (
    temp_dir,
    Capturing,
    verbose_print,
    remove_file,
    get_username,
    bin_data,
    create_hdf5,
    return_binary_c_version_info,
    parse_binary_c_version_info,
    output_lines,
    get_defaults,
    example_parse_output,
    create_arg_string,
    get_arg_keys,
    get_help,
    get_help_all,
    get_help_super,
    write_binary_c_parameter_descriptions_to_rst_file,
    make_build_text,
)
from binarycpython.utils.dicts import AutoVivificationDict, inspect_dict, merge_dicts
from binarycpython.utils.ensemble import (
    binaryc_json_serializer,
    handle_ensemble_string_to_json,
)

TMP_DIR = temp_dir("tests", "test_functions")


class dummy:
    """
    Dummy class to be used in the merge_dicts
    """

    def __init__(self, name):
        """
        init
        """
        self.name = name

    def __str__(self):
        """
        str returns self.name
        """
        return self.name


class test_verbose_print(unittest.TestCase):
    """
    Unittests for verbose_print
    """

    def test_print(self):
        with Capturing() as output:
            self._test_print()

    def _test_print(self):
        """
        Tests whether something gets printed
        """
        verbose_print("test1", 1, 0)

    def test_not_print(self):
        with Capturing() as output:
            self._test_not_print()

    def _test_not_print(self):
        """
        Tests whether nothing gets printed.
        """

        verbose_print("test1", 0, 1)


class test_remove_file(unittest.TestCase):
    """
    Unittests for remove_file
    """

    def test_remove_file(self):
        with Capturing() as output:
            self._test_remove_file()

    def _test_remove_file(self):
        """
        Test to remove a file
        """

        with open(os.path.join(TMP_DIR, "test_remove_file_file.txt"), "w") as f:
            f.write("test")

        remove_file(os.path.join(TMP_DIR, "test_remove_file_file.txt"))

    def test_remove_nonexisting_file(self):
        with Capturing() as output:
            self._test_remove_nonexisting_file()

    def _test_remove_nonexisting_file(self):
        """
        Test to try to remove a nonexistant file
        """

        file = os.path.join(TMP_DIR, "test_remove_nonexistingfile_file.txt")

        remove_file(file)


class test_temp_dir(unittest.TestCase):
    """
    Unittests for temp_dir
    """

    def test_create_temp_dir(self):
        with Capturing() as output:
            self._test_create_temp_dir()

    def _test_create_temp_dir(self):
        """
        Test making a temp directory and comparing that to what it should be
        """

        #
        binary_c_temp_dir = temp_dir()
        username = get_username()
        general_temp_dir = tempfile.gettempdir()

        # Get username
        username = get_username()
        dirname = "binary_c_python-{}".format(username)

        #
        self.assertTrue(
            os.path.isdir(
                os.path.join(general_temp_dir, "binary_c_python-{}".format(username))
            )
        )
        self.assertTrue(
            os.path.join(general_temp_dir, "binary_c_python-{}".format(username))
        ) == binary_c_temp_dir


class test_create_hdf5(unittest.TestCase):
    """
    Unittests for create_hdf5
    """

    def test_1(self):
        with Capturing() as output:
            self._test_1()

    def _test_1(self):
        """
        Test that creates files, packs them in a hdf5 file and checks the contents
        """

        testdir = os.path.join(TMP_DIR, "test_create_hdf5")
        os.makedirs(testdir, exist_ok=True)

        # Create dummy settings file:
        settings_dict = {"settings_1": 1, "settings_2": [1, 2]}

        with open(os.path.join(testdir, "example_settings.json"), "w") as f:
            f.write(json.dumps(settings_dict))

        with open(os.path.join(testdir, "data1.dat"), "w") as f:
            f.write("time mass\n")
            f.write("1 10")

        create_hdf5(testdir, "testhdf5.hdf5")
        file = h5py.File(os.path.join(testdir, "testhdf5.hdf5"), "r")

        self.assertIn(b"time", file.get("data/data1_header")[()])
        self.assertIn(b"mass", file.get("data/data1_header")[()])

        self.assertIn("settings_1", json.loads(file.get("settings/used_settings")[()]))
        self.assertIn("settings_2", json.loads(file.get("settings/used_settings")[()]))


class test_return_binary_c_version_info(unittest.TestCase):
    """
    Unittests for return_binary_c_version_info
    """

    def test_not_parsed(self):
        with Capturing() as output:
            self._test_not_parsed()

    def _test_not_parsed(self):
        """
        Test for the raw version_info output
        """

        version_info = return_binary_c_version_info(parsed=False)

        self.assertTrue(isinstance(version_info, str))
        self.assertIn("Build", version_info)
        self.assertIn("REIMERS_ETA_DEFAULT", version_info)
        self.assertIn("SIGMA_THOMPSON", version_info)

    def test_parsed(self):
        with Capturing() as output:
            self._test_parsed()

    def _test_parsed(self):
        """
        Test for the parssed version_info
        """

        # also tests the parse_version_info indirectly
        version_info_parsed = return_binary_c_version_info(parsed=True)

        self.assertTrue(isinstance(version_info_parsed, dict))
        self.assertIn("isotopes", version_info_parsed.keys())
        self.assertIn("argpairs", version_info_parsed.keys())
        self.assertIn("ensembles", version_info_parsed.keys())
        self.assertIn("macros", version_info_parsed.keys())
        self.assertIn("elements", version_info_parsed.keys())
        self.assertIn("dt_limits", version_info_parsed.keys())
        self.assertIn("nucleosynthesis_sources", version_info_parsed.keys())
        self.assertIn("miscellaneous", version_info_parsed.keys())


class test_parse_binary_c_version_info(unittest.TestCase):
    """
    Unittests for function parse_binary_c_version_info
    """

    def test_1(self):
        with Capturing() as output:
            self._test_1()

    def _test_1(self):
        """
        Test for the parsed versio info, more detailed
        """

        info = return_binary_c_version_info(parsed=False)
        parsed_info = parse_binary_c_version_info(info)

        self.assertIn("isotopes", parsed_info.keys())
        self.assertIn("argpairs", parsed_info.keys())
        self.assertIn("ensembles", parsed_info.keys())
        self.assertIn("macros", parsed_info.keys())
        self.assertIn("elements", parsed_info.keys())
        self.assertIn("dt_limits", parsed_info.keys())
        self.assertIn("nucleosynthesis_sources", parsed_info.keys())
        self.assertIn("miscellaneous", parsed_info.keys())

        self.assertIsNotNone(parsed_info["argpairs"])
        self.assertIsNotNone(parsed_info["ensembles"])
        self.assertIsNotNone(parsed_info["macros"])
        self.assertIsNotNone(parsed_info["dt_limits"])
        self.assertIsNotNone(parsed_info["miscellaneous"])

        if parsed_info["macros"]["NUCSYN"] == "on":
            self.assertIsNotNone(parsed_info["isotopes"])

            if parsed_info["macros"]["NUCSYN_ID_SOURCES"] == "on":
                self.assertIsNotNone(parsed_info["nucleosynthesis_sources"])


class test_output_lines(unittest.TestCase):
    """
    Unittests for function output_lines
    """

    def test_1(self):
        with Capturing() as output:
            self._test_1()

    def _test_1(self):
        """
        Test to check if the shape and contents of output_lines is correct
        """

        example_text = "hallo\ntest\n123"
        output_1 = output_lines(example_text)

        self.assertTrue(isinstance(output_1, list))
        self.assertIn("hallo", output_1)
        self.assertIn("test", output_1)
        self.assertIn("123", output_1)


class test_example_parse_output(unittest.TestCase):
    """
    Unittests for function example_parse_output
    """

    def test_normal_output(self):
        with Capturing() as output:
            self._test_normal_output()

    def _test_normal_output(self):
        """
        Test checking if parsed output with a custom logging line works correctly
        """

        # generate logging lines. Here you can choose whatever you want to have logged, and with what header
        # You can also decide to `write` your own logging_line, which allows you to write a more complex logging statement with conditionals.
        logging_line = 'Printf("MY_STELLAR_DATA time=%g mass=%g\\n", stardata->model.time, stardata->star[0].mass)'

        # Generate entire shared lib code around logging lines
        custom_logging_code = binary_c_log_code(logging_line)

        # Run system. all arguments can be given as optional arguments. the custom_logging_code is one of them and will be processed automatically.
        output = run_system(
            M_1=1,
            metallicity=0.002,
            M_2=0.1,
            separation=0,
            orbital_period=100000000000,
            custom_logging_code=custom_logging_code,
        )

        parsed_output = example_parse_output(output, "MY_STELLAR_DATA")

        self.assertIn("time", parsed_output)
        self.assertIn("mass", parsed_output)
        self.assertTrue(isinstance(parsed_output["time"], list))
        self.assertTrue(len(parsed_output["time"]) > 0)

    def test_mismatch_output(self):
        with Capturing() as output:
            self._test_mismatch_output()

    def _test_mismatch_output(self):
        """
        Test checking if parsed output with a mismatching headerline doesnt have any contents
        """

        # generate logging lines. Here you can choose whatever you want to have logged, and with what header
        # You can also decide to `write` your own logging_line, which allows you to write a more complex logging statement with conditionals.
        logging_line = 'Printf("MY_STELLAR_DATA time=%g mass=%g\\n", stardata->model.time, stardata->star[0].mass)'

        # Generate entire shared lib code around logging lines
        custom_logging_code = binary_c_log_code(logging_line)

        # Run system. all arguments can be given as optional arguments. the custom_logging_code is one of them and will be processed automatically.
        output = run_system(
            M_1=1,
            metallicity=0.002,
            M_2=0.1,
            separation=0,
            orbital_period=100000000000,
            custom_logging_code=custom_logging_code,
        )

        parsed_output = example_parse_output(output, "MY_STELLAR_DATA_MISMATCH")
        self.assertIsNone(parsed_output)


class test_get_defaults(unittest.TestCase):
    """
    Unittests for function get_defaults
    """

    def test_no_filter(self):
        with Capturing() as output:
            self._test_no_filter()

    def _test_no_filter(self):
        """
        Test checking if the defaults without filtering contains non-filtered content
        """

        output_1 = get_defaults()

        self.assertTrue(isinstance(output_1, dict))
        self.assertIn("colour_log", output_1.keys())
        self.assertIn("M_1", output_1.keys())
        self.assertIn("list_args", output_1.keys())
        self.assertIn("use_fixed_timestep_%d", output_1.keys())

    def test_filter(self):
        with Capturing() as output:
            self._test_filter()

    def test_filter(self):
        """
        Test checking filtering works correctly
        """

        # Also tests the filter_arg_dict indirectly
        output_1 = get_defaults(filter_values=True)

        self.assertTrue(isinstance(output_1, dict))
        self.assertIn("colour_log", output_1.keys())
        self.assertIn("M_1", output_1.keys())
        self.assertNotIn("list_args", output_1.keys())
        self.assertNotIn("use_fixed_timestep_%d", output_1.keys())


class test_get_arg_keys(unittest.TestCase):
    """
    Unittests for function get_arg_keys
    """

    def test_1(self):
        with Capturing() as output:
            self._test_1()

    def _test_1(self):
        """
        Test checking if some of the keys are indeed in the list
        """

        output_1 = get_arg_keys()

        self.assertTrue(isinstance(output_1, list))
        self.assertIn("colour_log", output_1)
        self.assertIn("M_1", output_1)
        self.assertIn("list_args", output_1)
        self.assertIn("use_fixed_timestep_%d", output_1)


class test_create_arg_string(unittest.TestCase):
    """
    Unittests for function create_arg_string
    """

    def test_default(self):
        with Capturing() as output:
            self._test_default()

    def _test_default(self):
        """
        Test checking if the argstring is correct
        """

        input_dict = {"separation": 40000, "M_1": 10}
        argstring = create_arg_string(input_dict)
        self.assertEqual(argstring, "separation 40000 M_1 10")

    def test_sort(self):
        with Capturing() as output:
            self._test_sort()

    def _test_sort(self):
        """
        Test checking if the argstring with a different ordered dict is also in a differnt order
        """

        input_dict = {"M_1": 10, "separation": 40000}
        argstring = create_arg_string(input_dict, sort=True)
        self.assertEqual(argstring, "M_1 10 separation 40000")

    def test_filtered(self):
        with Capturing() as output:
            self._test_filtered()

    def _test_filtered(self):
        """
        Test if filtering works
        """

        input_dict = {"M_1": 10, "separation": 40000, "list_args": "NULL"}
        argstring = create_arg_string(input_dict, filter_values=True)
        self.assertEqual(argstring, "M_1 10 separation 40000")


class test_get_help(unittest.TestCase):
    """
    Unit tests for function get_help
    """

    def test_input_normal(self):
        with Capturing() as output:
            self._test_input_normal()

    def _test_input_normal(self):
        """
        Function to test the get_help function
        """

        self.assertEqual(
            get_help("M_1", print_help=False)["parameter_name"],
            "M_1",
            msg="get_help('M_1') should return the correct parameter name",
        )

    def test_no_input(self):
        with Capturing() as output:
            self._test_no_input()

    def _test_no_input(self):
        """
        Test if the result is None if called without input
        """

        output = get_help()
        self.assertIsNone(output)

    def test_wrong_input(self):
        with Capturing() as output:
            self._test_wrong_input()

    def _test_wrong_input(self):
        """
        Test if the result is None if called with an unknown input
        """

        output = get_help("kaasblokjes")
        self.assertIsNone(output)

    # def test_print(self):
    #     output = get_help("M_1", print_help=True)


class test_get_help_all(unittest.TestCase):
    """
    Unit test for get_help_all
    """

    def test_all_output(self):
        with Capturing() as output:
            self._test_all_output()

    def _test_all_output(self):
        """
        Function to test the get_help_all function
        """

        get_help_all_output = get_help_all(print_help=False)
        get_help_all_keys = get_help_all_output.keys()

        self.assertIn("stars", get_help_all_keys, "missing section")
        self.assertIn("binary", get_help_all_keys, "missing section")
        self.assertIn("nucsyn", get_help_all_keys, "missing section")
        self.assertIn("output", get_help_all_keys, "missing section")
        self.assertIn("i/o", get_help_all_keys, "missing section")
        self.assertIn("algorithms", get_help_all_keys, "missing section")
        self.assertIn("misc", get_help_all_keys, "missing section")

    # def test_print(self):
    #     # test if stuff is printed
    #     get_help_all(print_help=True)


class test_get_help_super(unittest.TestCase):
    """
    Unit test for get_help_super
    """

    def test_all_output(self):
        with Capturing() as output:
            self._test_all_output()

    def _test_all_output(self):
        """
        Function to test the get_help_super function
        """

        get_help_super_output = get_help_super()
        get_help_super_keys = get_help_super_output.keys()

        self.assertIn("stars", get_help_super_keys, "missing section")
        self.assertIn("binary", get_help_super_keys, "missing section")
        self.assertIn("nucsyn", get_help_super_keys, "missing section")
        self.assertIn("output", get_help_super_keys, "missing section")
        self.assertIn("i/o", get_help_super_keys, "missing section")
        self.assertIn("algorithms", get_help_super_keys, "missing section")
        self.assertIn("misc", get_help_super_keys, "missing section")

    # def test_print(self):
    #     # test to see if stuff is printed.
    #     get_help_super(print_help=True)


class test_make_build_text(unittest.TestCase):
    """
    Unittests for function
    """

    def test_output(self):
        with Capturing() as output:
            self._test_output()

    def _test_output(self):
        """
        Test checking the contents of the build_text
        """

        build_text = make_build_text()

        # Remove the things
        build_text = build_text.replace("**binary_c git branch**:", ";")
        build_text = build_text.replace("**binary_c git revision**:", ";")
        build_text = build_text.replace("**Built on**:", ";")

        # Split up
        split_text = build_text.split(";")

        # Check whether the contents are actually there
        self.assertNotEqual(split_text[1].strip(), "second")
        self.assertNotEqual(split_text[2].strip(), "second")
        self.assertNotEqual(split_text[3].strip(), "second")


class test_write_binary_c_parameter_descriptions_to_rst_file(unittest.TestCase):
    """
    Unittests for function write_binary_c_parameter_descriptions_to_rst_file
    """

    def test_bad_outputname(self):
        with Capturing() as output:
            self._test_bad_outputname()

    def _test_bad_outputname(self):
        """
        Test checking if None is returned when a bad input name is provided
        """

        output_name = os.path.join(
            TMP_DIR,
            "test_write_binary_c_parameter_descriptions_to_rst_file_test_1.txt",
        )
        output_1 = write_binary_c_parameter_descriptions_to_rst_file(output_name)
        self.assertIsNone(output_1)

    def test_checkfile(self):
        with Capturing() as output:
            self._test_checkfile()

    def _test_checkfile(self):
        """
        Test checking if the file is created correctly
        """

        output_name = os.path.join(
            TMP_DIR,
            "test_write_binary_c_parameter_descriptions_to_rst_file_test_1.rst",
        )
        output_1 = write_binary_c_parameter_descriptions_to_rst_file(output_name)
        self.assertTrue(os.path.isfile(output_name))


class test_inspect_dict(unittest.TestCase):
    """
    Unittests for function inspect_dict
    """

    def test_compare_dict(self):
        with Capturing() as output:
            self._test_compare_dict()

    def _test_compare_dict(self):
        """
        Test checking if inspect_dict returns the correct structure by comparing it to known value
        """

        input_dict = {
            "int": 1,
            "float": 1.2,
            "list": [1, 2, 3],
            "function": os.path.isfile,
            "dict": {"int": 1, "float": 1.2},
        }
        output_dict = inspect_dict(input_dict)
        compare_dict = {
            "int": int,
            "float": float,
            "list": list,
            "function": os.path.isfile.__class__,
            "dict": {"int": int, "float": float},
        }
        self.assertTrue(compare_dict == output_dict)

    def test_compare_dict_with_print(self):
        with Capturing() as output:
            self._test_compare_dict_with_print()

    def _test_compare_dict_with_print(self):
        """
        Test checking output is printed
        """

        input_dict = {
            "int": 1,
            "float": 1.2,
            "list": [1, 2, 3],
            "function": os.path.isfile,
            "dict": {"int": 1, "float": 1.2},
        }
        output_dict = inspect_dict(input_dict, print_structure=True)


class test_merge_dicts(unittest.TestCase):
    """
    Unittests for function merge_dicts
    """

    def test_empty(self):
        with Capturing() as output:
            self._test_empty()

    def _test_empty(self):
        """
        Test merging an empty dict
        """

        input_dict = {
            "int": 1,
            "float": 1.2,
            "list": [1, 2, 3],
            "function": os.path.isfile,
            "dict": {"int": 1, "float": 1.2},
        }
        dict_2 = {}
        output_dict = merge_dicts(input_dict, dict_2)
        self.assertTrue(output_dict == input_dict)

    def test_unequal_types(self):
        with Capturing() as output:
            self._test_unequal_types()

    def _test_unequal_types(self):
        """
        Test merging unequal types: should raise valueError
        """

        dict_1 = {"input": 10}
        dict_2 = {"input": "hello"}

        self.assertRaises(ValueError, merge_dicts, dict_1, dict_2)

    def test_bools(self):
        with Capturing() as output:
            self._test_bools()

    def _test_bools(self):
        """
        Test merging dict with booleans
        """

        dict_1 = {"bool": True}
        dict_2 = {"bool": False}
        output_dict = merge_dicts(dict_1, dict_2)

        self.assertTrue(isinstance(output_dict["bool"], bool))
        self.assertTrue(output_dict["bool"])

    def test_ints(self):
        with Capturing() as _:
            self._test_ints()

    def _test_ints(self):
        """
        Test merging dict with ints
        """

        dict_1 = {"int": 2}
        dict_2 = {"int": 1}
        output_dict = merge_dicts(dict_1, dict_2)

        self.assertTrue(isinstance(output_dict["int"], int))
        self.assertEqual(output_dict["int"], 3)

    def test_floats(self):
        with Capturing() as output:
            self._test_floats()

    def _test_floats(self):
        """
        Test merging dict with floats
        """

        dict_1 = {"float": 4.5}
        dict_2 = {"float": 4.6}
        output_dict = merge_dicts(dict_1, dict_2)

        self.assertTrue(isinstance(output_dict["float"], float))
        self.assertEqual(output_dict["float"], 9.1)

    def test_lists(self):
        with Capturing() as output:
            self._test_lists()

    def _test_lists(self):
        """
        Test merging dict with lists
        """

        dict_1 = {"list": [1, 2]}
        dict_2 = {"list": [3, 4]}
        output_dict = merge_dicts(dict_1, dict_2)

        self.assertTrue(isinstance(output_dict["list"], list))
        self.assertEqual(output_dict["list"], [1, 2, 3, 4])

    def test_dicts(self):
        with Capturing() as _:
            self._test_dicts()

    def _test_dicts(self):
        """
        Test merging dict with dicts
        """

        dict_1 = {"dict": {"same": 1, "other_1": 2.0}}
        dict_2 = {"dict": {"same": 2, "other_2": [4.0]}}
        output_dict = merge_dicts(dict_1, dict_2)

        self.assertTrue(isinstance(output_dict["dict"], dict))
        self.assertEqual(
            output_dict["dict"], {"same": 3, "other_1": 2.0, "other_2": [4.0]}
        )

    def test_unsupported(self):
        with Capturing() as output:
            self._test_unsupported()

    def _test_unsupported(self):
        """
        Test merging dict with unsupported types. should raise ValueError
        """

        dict_1 = {"new": dummy("david")}
        dict_2 = {"new": dummy("gio")}

        # output_dict = merge_dicts(dict_1, dict_2)
        self.assertRaises(ValueError, merge_dicts, dict_1, dict_2)


class test_binaryc_json_serializer(unittest.TestCase):
    """
    Unittests for function binaryc_json_serializer
    """

    def test_not_function(self):
        with Capturing() as output:
            self._test_not_function()

    def _test_not_function(self):
        """
        Test passing an object that doesnt get turned in to a string
        """

        stringo = "hello"
        output = binaryc_json_serializer(stringo)
        self.assertTrue(stringo == output)

    def test_function(self):
        with Capturing() as output:
            self._test_function()

    def _test_function(self):
        """
        Test passing an object that gets turned in to a string: a function
        """

        string_of_function = str(os.path.isfile)
        output = binaryc_json_serializer(os.path.isfile)
        self.assertTrue(string_of_function == output)


class test_handle_ensemble_string_to_json(unittest.TestCase):
    """
    Unittests for function handle_ensemble_string_to_json
    """

    def test_1(self):
        with Capturing() as _:
            self._test_1()

    def _test_1(self):
        """
        Test passing string representation of a dictionary.
        """

        _ = str(os.path.isfile)
        input_string = '{"ding": 10, "list_example": [1,2,3]}'
        output_dict = handle_ensemble_string_to_json(input_string)

        self.assertTrue(isinstance(output_dict, dict))
        self.assertTrue(output_dict["ding"] == 10)
        self.assertTrue(output_dict["list_example"] == [1, 2, 3])


class test_AutoVivicationDict(unittest.TestCase):
    """
    Unittests for AutoVivicationDict
    """

    def test_add(self):
        """
        Tests to see if the adding is done correctly
        """

        result_dict = AutoVivificationDict()

        result_dict["a"]["b"]["c"] += 10

        self.assertEqual(result_dict["a"]["b"]["c"], 10)
        result_dict["a"]["b"]["c"] += 10
        self.assertEqual(result_dict["a"]["b"]["c"], 20)


class test_bin_data(unittest.TestCase):
    """
    Unittests for bin_data
    """

    def test_positive_bin(self):
        """
        Tests to see if the binning is done correctly for positive values
        """

        value = 0.6
        binwidth = 1

        binned_value = bin_data(value, binwidth)

        self.assertEqual(binned_value, 0.5)

    def test_negative_bin(self):
        """
        Tests to see if the binning is done correctly for negative values
        """

        value = -0.6
        binwidth = 1

        binned_value = bin_data(value, binwidth)

        self.assertEqual(binned_value, -0.5)

    def test_zero_bin(self):
        """
        Tests to see if the binning is done correctly
        TODO: when the value is 0 then its now binned in the negative located bin. Decide whether we want that
        """

        value = 0
        binwidth = 1

        binned_value = bin_data(value, binwidth)

        self.assertEqual(binned_value, -0.5)


if __name__ == "__main__":
    unittest.main()
