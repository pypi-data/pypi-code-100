import os
import re

import numpy as np

from sknrf.app.dataviewer.model.mdif import MDIF, MDIFGroup, MDIFBlock
from sknrf.utilities.numeric import lin_deg2re_im


class LPCBlock(MDIFBlock):
    pass


class LPCGroup(MDIFGroup):
    pass


class LPC(MDIF):
    parameter_type_map = {
                          "File": "string",
                          "Comment": "string",
                          "Date": "string",
                          "Frequency": "int",
                          "Char.Impedances": "complex",
                          "Source Impedance": "complex",
                          "Source Impedance (Polar)": "complex",
                          "Source Frequencies": "complex",
                          "Source Impedances": "complex",
                          "Source Impedances (Polar)": "complex",
                          "Load Frequencies": "complex",
                          "Setup": "string",
                          "Reference Plane": "string",
                          "Gamma/Phi": "string"
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
        root = LPC(name=filename)
        tokenizer = re.compile(r'("[^"]*"|[^\s=:]+)')
        group = None
        block_name, comments_finished, inside_block = "LoadPull", False, False
        sweep_names, sweep_types, sweep_values = [], [], []
        attribute_names, attribute_types, attribute_values = [], [], []
        dependent_names, dependent_types, dependent_values = [], [], []
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
                        if tokens[0].startswith("!"):  # Comment | Attributes
                            tokens[0] = tokens[0].strip("!")
                            if not tokens[0]:
                                del tokens[0]
                            if " ".join(tokens[0:1]).startswith("File"):
                                pass
                            elif " ".join(tokens[0:1]).startswith("Comment"):
                                pass
                            elif " ".join(tokens[0:1]).startswith("Date"):
                                pass
                            elif " ".join(tokens[0:1]).startswith("Frequency"):
                                name, value, scale = tokens
                                type_ = "real"
                                scale = scale.upper()
                                attribute_names.append(name)
                                attribute_types.append(type_)
                                attribute_values.append(LPC.type_value_map[type_](value) * LPC.freq_scale_map[scale])
                                attribute_names.append("freq_scale")
                                attribute_types.append("string")
                                attribute_values.append(scale)
                            elif " ".join(tokens[0:1]).startswith("Char.Impedances"):
                                pass
                            elif " ".join(tokens[0:2]).startswith("Source Impedance"):
                                pass
                            elif " ".join(tokens[0:3]).startswith("Source Impedance (Polar)"):
                                pass
                            elif " ".join(tokens[0:2]).startswith("Source Frequencies"):
                                pass
                            elif " ".join(tokens[0:2]).startswith("Source Impedances"):
                                pass
                            elif " ".join(tokens[0:3]).startswith("Source Impedances (Polar)"):
                                pass
                            elif " ".join(tokens[0:2]).startswith("Load Frequencies"):
                                pass
                            elif " ".join(tokens[0:1]).startswith("Setup"):
                                pass
                            elif " ".join(tokens[0:2]).startswith("Reference Plane"):
                                pass
                            elif " ".join(tokens[0:1]).startswith("Gamma/Phi"):
                                pass
                            else:  # Comment
                                pass
                        elif tokens[0].startswith("#"):  # Sweep (Dependents)
                            del tokens[0]
                            if sweep_names and sweep_types:
                                # Save previous block
                                block = LPCBlock(sweep=sweep_values, attribute=attribute_values)
                                dependent_array = np.asarray(dependent_values, dtype="S25")
                                block.independent = dependent_array[:, 0].astype(np.float64)
                                block.dependents = dependent_array[:, 1:].astype(np.complex)
                                group.data.append(block)
                                block_name = ""
                                sweep_values = []
                                attribute_values = []
                                dependent_values = []
                            else:
                                sweep_names = [dependent_names[0]] + dependent_names[1:len(tokens):2]
                                sweep_types = ["real"] + ["complex"]*(len(sweep_names)-1)
                                del dependent_names[0:len(tokens)]
                                del dependent_types[0:len(tokens)]
                                group = LPCGroup(block_name,
                                                 sweeps=sweep_names, sweep_types=sweep_types,
                                                 attributes=attribute_names, attribute_types=attribute_types,
                                                 independent=dependent_names[0], independent_type=dependent_types[0],
                                                 dependents=dependent_names[1:], dependent_types=dependent_types[1:])
                            # Prepare new block
                            for index, type_ in zip(range(len(sweep_names)), sweep_types):
                                if index == 0:
                                    block_name = tokens[0]
                                if type_ in ("3", "complex"):
                                    sweep_value = lin_deg2re_im(LPC.type_value_map[type_](tokens[0], tokens[1]))
                                    sweep_values.append(sweep_value)
                                    del tokens[0:2]
                                else:
                                    sweep_values.append(LPC.type_value_map[type_](tokens[0]))
                                    del tokens[0]
                        else:  # Dependents
                            if inside_block:
                                dependent_values.append(tokens)
                            else:
                                for index in range(0, len(tokens)):
                                    dependent_names.append(tokens[index])
                                    dependent_types.append("real")
                                inside_block = True
                except Exception as e:
                    raise type(e)("%s when reading line: %d, %s" % (str(e), line_num, line))
                    # Save previous block
            block = LPCBlock(sweep=sweep_values, attribute=attribute_values)
            dependent_array = np.asarray(dependent_values, dtype="S25")
            block.independent = dependent_array[:, 0].astype(np.float64)
            block.dependents = dependent_array[:, 1:].astype(np.complex)
            if group is None:
                group = LPCGroup(block_name,
                                 attributes=attribute_names, attribute_types=attribute_types,
                                 independent=dependent_names[0], independent_type=dependent_types[0],
                                 dependents=dependent_names[1:], dependent_types=dependent_types[1:])
            group.data.append(block)
            root.dataBlocks.append(group)
            return root

    @staticmethod
    def import_dataset(filename):
        return MDIF.import_dataset(filename, "LoadPull", class_=LPC)

    def write(self, filename):
        with open(filename, "w") as f:
            f.write("!=========================================================================\n")
            f.write("! %s\n" % (os.path.split(filename)[1], ))
            f.write("! %s\n\n" % (self.date, ))

            for group in self.dataBlocks:
                sweep_names = group.sweeps
                sweep_types = group.sweep_types
                dependent_names = group.dependents
                dependent_types = group.dependent_types
                for name in sweep_names:
                    f.write("%s " % (name,))
                for name in dependent_names:
                    f.write("%s " % (name,))
                f.write("\n")
                for block in group.data:
                    sweep_values = block.sweep
                    f.write("# ")
                    for index, type_ in zip(range(len(sweep_names)), sweep_types):
                        f.write("%s " % (LPC.type_string_map[type_](sweep_values[index]),))
                    f.write("\n")
                    if dependent_names:
                        dependent_values = block.dependents.astype(np.float)
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

    read_filename = os.sep.join((Settings().root, "data", "test", "lpc", "load_pull.lpcwave"))
    write_filename = os.sep.join((Settings().root, "data", "test", "lpc", "load_pull_write.lpcwave"))
    root_ = LPC.read(read_filename)
    root_.write(write_filename)
    dataset = LPC.import_dataset(read_filename)