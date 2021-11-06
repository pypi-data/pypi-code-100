import os
import re

import numpy as np

from sknrf.app.dataviewer.model.mdif import MDIF, MDIFGroup, MDIFBlock


class SPLBlock(MDIFBlock):
    pass


class SPLGroup(MDIFGroup):
    pass


class SPL(MDIF):
    parameter_type_map = {
                          "Number of power meters": "int",
                          "number of positions": "int",
                          "DUT s-para": "bool",
                          "User params": "int",
                          "User names": "string",
                          "User units": "string",
                          "Gamma_dut": "string",
                          "Source": "complex",
                          "Source_2nd": "complex",
                          "Source_3rd": "complex",
                          "Load": "complex",
                          "Load_2nd": "complex",
                          "Load_3rd": "complex",
                          }
    parameter_args_map = {
                          "Number of power meters": 1,
                          "number of positions": 1,
                          "DUT s-para": 1,
                          "User params": 1,
                          "User names": 2,
                          "User units": 2,
                          "Gamma_dut": 0,
                          "Source": 2,
                          "Source_2nd": 2,
                          "Source_3rd": 2,
                          "Load": 2,
                          "Load_2nd": 2,
                          "Load_3rd": 2,
                          }

    freq_scale_map = {"HZ": 1,
                      "KHZ": 1e3,
                      "MHZ": 1e6,
                      "GHZ": 1e9}

    scale_freq_map = {1: "HZ",
                      1e3: "KHZ",
                      1e6: "MHZ",
                      1e9: "GHZ"
                      }

    @staticmethod
    def read(filename):
        root = SPL(name=filename)
        tokenizer = re.compile(r'("[^"]*"|[^\s=:]+)')
        block_name, comments_finished, inside_block = "", False, False
        sweep_names, sweep_types, sweep_values = [], [], []
        attribute_names, attribute_types, attribute_values = [], [], []
        dependent_names, dependent_types, dependent_values = [], [], []
        num_user_params = 0
        line_num = 0

        with open(filename) as f:
            for line in iter(f):
                try:
                    line = line.strip()
                    line_num += 1
                    if not line:
                        pass
                    else:
                        # # Tokenize the Input
                        # tokens = list(tokenizer.findall(line))
                        tokens = [m.group(0) for m in tokenizer.finditer(line)]
                        if not inside_block:
                            if tokens[0].startswith("!"):  # Comment | Dependent Names
                                tokens[0] = tokens[0].strip("!")
                                if not tokens[0]:
                                    del tokens[0]
                                if comments_finished:  # Dependent Names
                                    inside_block = True
                                    for index in range(0, len(tokens)):
                                        dependent_names.append(tokens[index])
                                else:  # Comment
                                    pass
                            else:
                                comments_finished = True
                                while tokens:
                                    if tokens[0].startswith("Frequency"):
                                        name, value, scale = tokens[0:3]
                                        type_ = "real"
                                        scale = scale.upper()
                                        del tokens[0:3]
                                        attribute_names.append(name)
                                        attribute_types.append(type_)
                                        attribute_values.append(SPL.type_value_map[type_](value)*SPL.freq_scale_map[scale])
                                        attribute_names.append("freq_scale")
                                        attribute_types.append("string")
                                        attribute_values.append(scale)
                                    elif tokens[0].startswith(("Source", "Gamma_source")):
                                        name, real, imag = tokens[0], tokens[1], tokens[2]
                                        type_ = "complex"
                                        del tokens[0:3]
                                        attribute_names.append(name)
                                        attribute_types.append(type_)
                                        attribute_values.append(SPL.type_value_map[type_](real, imag))
                                    elif tokens[0].startswith(("Load", "Gamma_load")):
                                        name, real, imag = tokens[0], tokens[1], tokens[2]
                                        type_ = "complex"
                                        del tokens[0:3]
                                        attribute_names.append(name)
                                        attribute_types.append(type_)
                                        attribute_values.append(SPL.type_value_map[type_](real, imag))
                                    elif tokens[0].startswith("Pin_avail_src"):
                                        name, value, scale = tokens[0:3]
                                        type_ = "real"
                                        del tokens[0:3]
                                        attribute_names.append(name)
                                        attribute_types.append(type_)
                                        attribute_values.append(SPL.type_value_map[type_](value))
                                    elif " ".join(tokens[0:4]).startswith("Number of power meters"):
                                        name, value = " ".join(tokens[0:4]), tokens[4]
                                        type_ = "int"
                                        del tokens[0:5]
                                        attribute_names.append(name)
                                        attribute_types.append(type_)
                                        attribute_values.append(SPL.type_value_map[type_](value))
                                    elif " ".join(tokens[0:3]).startswith("number of positions"):
                                        name, value = " ".join(tokens[0:3]), tokens[3]
                                        type_ = "int"
                                        del tokens[0:4]
                                        attribute_names.append(name)
                                        attribute_types.append(type_)
                                        attribute_values.append(SPL.type_value_map[type_](value))
                                    elif " ".join(tokens[0:2]).startswith("DUT s-para"):
                                        name, value = " ".join(tokens[0:2]), tokens[2]
                                        type_ = "string"
                                        del tokens[0:3]
                                        attribute_names.append(name)
                                        attribute_types.append(type_)
                                        attribute_values.append(SPL.type_value_map[type_](value))
                                    elif " ".join(tokens[0:2]).startswith("User params"):
                                        name, value = " ".join(tokens[0:2]), tokens[2]
                                        type_ = "int"
                                        del tokens[0:3]
                                        attribute_names.append(name)
                                        attribute_types.append(type_)
                                        attribute_values.append(SPL.type_value_map[type_](value))
                                        num_user_params = attribute_values[-1]
                                    elif " ".join(tokens[0:2]).startswith("User names"):
                                        name, value = " ".join(tokens[0:2]), " ".join(tokens[2:2+num_user_params+1])
                                        type_ = "string"
                                        del tokens[0:2+num_user_params+2]
                                        attribute_names.append(name)
                                        attribute_types.append(type_)
                                        attribute_values.append(SPL.type_value_map[type_](value))
                                    elif " ".join(tokens[0:2]).startswith("User units"):
                                        name, value = " ".join(tokens[0:2]), " ".join(tokens[2:2 + num_user_params + 1])
                                        type_ = "string"
                                        del tokens[0:2 + num_user_params + 2]
                                        attribute_names.append(name)
                                        attribute_types.append(type_)
                                        attribute_values.append(SPL.type_value_map[type_](value))
                                    elif tokens[0].startswith("Gamma_dut"):
                                        del tokens[0]
                                    elif " ".join(tokens[0:2]).startswith("Measured parameters"):  # Ignore
                                        del tokens[:]
                                    else:
                                        raise IOError("Unrecognized attribute: %s" % (tokens[0], ))
                        else:  # Attribute | Dependent Values
                            dependent_values.append(tokens)
                except Exception as e:
                    raise type(e)("%s when reading line: %d, %s" % (str(e), line_num, line))

            block = SPLBlock(sweep=sweep_values, attribute=attribute_values)
            dependent_array = np.asarray(dependent_values, dtype="S25")
            block.dependents = dependent_array.astype(np.float64)
            group = SPLGroup(block_name,
                             sweeps=sweep_names, sweep_types=sweep_types,
                             attributes=attribute_names, attribute_types=attribute_types,
                             dependents=dependent_names, dependent_types=dependent_types,
                             data=[block])
            root.dataBlocks.append(group)
            return root

    def write(self, filename):
        with open(filename, "w") as f:
            f.write("!=========================================================================\n")
            f.write("! %s\n" % (os.path.split(filename)[1], ))
            f.write("! %s\n\n" % (self.date, ))

            for group in self.dataBlocks:
                dependent_names = group.dependents
                dependent_types = group.dependent_types
                for block in group.data:
                    freq = block.attribute[0]/SPL.freq_scale_map[block.attribute[1]]
                    f.write("Frequency    %f %s\n" % (freq, block.attribute[1]))
                    for name, type_, value in zip(group.attributes[2:], group.attribute_types[2:], block.attribute[2:]):
                        f.write("%s: %s\n" % (name, SPL.type_string_map[type_](value)))
                    if dependent_names:
                        f.write("! ")
                        for name in dependent_names:
                            f.write("%s " % (name, ))
                        f.write("\n")
                        dependent_values = block.dependents
                        print_options = np.get_printoptions()
                        format_ = {'float_kind': lambda x: "%12.8f" % x,
                                   'complex_kind': lambda x: "%12.8f%12.8f" % (x.real, x.imag)}
                        np.set_printoptions(precision=8, threshold=np.nan, formatter=format_)
                        dependent_str = np.array_str(dependent_values, np.inf, True).replace("[", " ").replace("]", " ")
                        np.set_printoptions(**print_options)
                        f.write("%s\n" % (dependent_str,))
                f.write("\n")


if __name__ == '__main__':
    from sknrf.settings import Settings

    read_filename = os.sep.join((Settings().root, "data", "test", "spl", "load_pull2.lp"))
    write_filename = os.sep.join((Settings().root, "data", "test", "spl", "load_pull2_write.lp"))
    root_ = SPL.read(read_filename)
    root_.write(write_filename)
