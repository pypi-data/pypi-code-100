import os
from os import walk
import csv
import yaml
import pickle

import numpy as np

from sknrf.settings import Settings
from sknrf.enums.mipi import MIPI_WRITE_MODE, MIPI_DATA_LIMIT, MIPI_ADDRESS_LIMIT
from sknrf.enums.modulation import TECH, ET
from sknrf.enums.modulation import GSM_BAND, GSM_BW, GSM_RB
from sknrf.enums.modulation import CDMA_BAND, CDMA_BW, CDMA_RB
from sknrf.enums.modulation import WCDMA_BAND, WCDMA_BW, WCDMA_RB
from sknrf.enums.modulation import LTE_BAND, LTE_BW, LTE_RB
from sknrf.enums.modulation import tech2band_map, tech2bw_map, rb2bw_map

qcom2bcom_map = {
    "Reg_Write_ExtL1":  MIPI_WRITE_MODE.BASIC,
    "Reg_Write_ExtL4":  MIPI_WRITE_MODE.EXTENDED,
    "Reg_Write_ExtL16": MIPI_WRITE_MODE.EXTENDED_LONG,
    "Delay_uS":         MIPI_WRITE_MODE.DELAY
}


def convert_mipi(code_list):
    new_list = []
    for code in code_list:
        if len(code) > 0 and not code[0].startswith("#"):
            write_mode = qcom2bcom_map[code[0]]
            if len(code[1]) > 0:
                address, data = int(code[1], 16), int(code[2], 16)
                if address <= MIPI_ADDRESS_LIMIT.BASIC and data <= MIPI_DATA_LIMIT.BASIC:
                    write_mode = MIPI_WRITE_MODE.BASIC
                elif address <= MIPI_ADDRESS_LIMIT.EXTENDED and data <= MIPI_DATA_LIMIT.EXTENDED:
                    write_mode = MIPI_WRITE_MODE.EXTENDED
                elif address <= MIPI_ADDRESS_LIMIT.EXTENDED_LONG and data <= MIPI_DATA_LIMIT.EXTENDED_LONG:
                    write_mode = MIPI_WRITE_MODE.EXTENDED_LONG
                else:
                    raise ValueError("MIPI address exceeds the maximum writeable address")

            if write_mode == MIPI_WRITE_MODE.DELAY:
                code = [write_mode.value, 0x00, int(code[2], 10)]
            else:
                code = [write_mode.value, int(code[1], 16), int(code[2], 16)]
            new_list.append(code)
    return new_list


def create_config(scripts_dirname, tx_enable_filename, tx_on_filename, config_filename):
    board, version = "qet5100", "v1p0"
    generic_program_keys = {"sleep": "%s_%s_%s" % (board, version, "GOTO_SLEEP"),
                            "power_up": "%s_%s_%s" % (board, version, "POWER_UP"),
                            "wake_up": "%s_%s_%s" % (board, version, "WAKE_UP"),
                            "standby": "%s_%s_%s" % (board, version, "TX_STANDBY"),
                            "alarm": "%s_%s_%s" % (board, version, "ALARM_REG_READ_ONLY"),
                            "tx_disable": "%s_%s_%s" % (board, version, "TX_DISABLE"),
                            "ecm_enable": "%s_%s_%s" % (board, version, "ECM_ENABLE"),
                            "ecm_disable": "%s_%s_%s" % (board, version, "ECM_DISABLE"),}
    generic_mipi_map = {"sleep": [], "power_up": [], "wake_up": [], "standby": [],
                        "alarm": [], "tx_disable": [], "ecm_enable": [], "ecm_disable": []}
    program_keys = {"tx_enable": "%s_%s_%s" % (board, version, "TECH_TX_ENABLE"),
                    "tx_on": "%s_%s_%s" % (board, version, "TX_ON")}
    program_map = {"tx_enable": [], "tx_on": [], "port_name": ""}
    mipi_map = {}
    scripts_filenames = []
    for (_, _, filenames) in walk(scripts_dirname):
        scripts_filenames += filenames

    # Create the config file dictionaries
    for tech in TECH:
        tech_name = tech.name.lower()
        mipi_map[tech_name] = {}
        for mode in ET:
            mode_name = mode.name.lower()
            mipi_map[tech_name][mode_name] = {}
            for band in tech2band_map[tech]:
                band_name = band.name.lower()
                mipi_map[tech_name][mode_name][band_name] = {}
                for bw in tech2bw_map[band.__class__]:
                    bw_name = bw.name.lower()
                    mipi_map[tech_name][mode_name][band_name][bw_name] = {}
                    for rb in bw2rb_map[bw.__class__]:
                        rb_name = rb.name.lower()
                        mipi_map[tech_name][mode_name][band_name][bw_name][rb_name] = program_map.copy()

    # TX Enable Scripts
    with open(tx_enable_filename, 'rt') as f:
        tx_enable_map = {k: v for k, v in list(csv.reader(f))}
    for k, v in tx_enable_map.items():
        v = v.strip()
        k_list = k.lower().split('-')
        port_name, tech_name, band_name, bw_name = k_list
        tech = TECH.__members__[tech_name.upper()]
        bw_name = "bw_" + bw_name
        with open(os.sep.join((scripts_dirname, v)), 'rt') as f:
            codes = list(csv.reader(f))
            codes = convert_mipi(codes)
            for mode in ET:
                mode_name = mode.name.lower()
                for rb in bw2rb_map[tech2bw_map[tech2band_map[tech]]]:
                    rb_name = rb.name.lower()
                    mipi_map[tech_name][mode_name][band_name][bw_name][rb_name]["tx_enable"] = codes
                    mipi_map[tech_name][mode_name][band_name][bw_name][rb_name]["port_name"] = port_name
        try:
            del scripts_filenames[scripts_filenames.index(v)]
        except ValueError:
            pass

    # TX On Scripts
    with open(tx_on_filename, 'rt') as f:
        tx_on_map = {k: v for k, v in list(csv.reader(f))}
    for k, v in tx_on_map.items():
        v = v.strip()
        k_list = k.lower().split('-')
        if len(k_list) == 4:  # APT MODE
            mode_name, port_name, tech_name, band_name = k_list
            tech = TECH.__members__[tech_name.upper()]
            bw_list = tech2bw_map[tech2band_map[tech]]
            rb_list = bw2rb_map[tech2bw_map[tech2band_map[tech]]]
        elif len(k_list) == 5:  # ET MODE
            mode_name, port_name, tech_name, band_name, rb_name = k_list
            tech = TECH.__members__[tech_name.upper()]
            if tech is TECH.LTE:
                bw_list = tech2bw_map[tech2band_map[tech]]
                rb_list = [bw2rb_map[tech2bw_map[tech2band_map[tech]]].__members__[rb_name.replace("rb", "rb_").upper()]]
            else:
                bw_list = [tech2bw_map[tech2band_map[tech]].__members__[("bw_" + rb_name).upper()]]
                rb_list = bw2rb_map[tech2bw_map[tech2band_map[tech]]]
        else:
            raise ValueError("Unknown TX ON Setting")
        with open(os.sep.join((scripts_dirname, v)), 'rt') as f:
            codes = list(csv.reader(f))
            codes = convert_mipi(codes)
            for bw in bw_list:
                bw_name = bw.name.lower()
                for rb in rb_list:
                    rb_name = rb.name.lower()
                    mipi_map[tech_name][mode_name][band_name][bw_name][rb_name]["tx_on"] = codes
                    mipi_map[tech_name][mode_name][band_name][bw_name][rb_name]["port_name"] = port_name
        try:
            del scripts_filenames[scripts_filenames.index(v)]
        except ValueError:
            pass

    # Workarounds
    # line 524: For B28B use B28 settings
    for tech in [TECH.LTE]:
        tech_name = tech.name.lower()
        for mode in ET:
            mode_name = mode.name.lower()
            mipi_map[tech_name][mode_name]["b28a"] = mipi_map[tech_name][mode_name]["b28"]
            mipi_map[tech_name][mode_name]["b28b"] = mipi_map[tech_name][mode_name]["b28"]

    # line 533: We don't have settings for 1.4M and 3M - change to 5M....
    for tech in [TECH.LTE]:
        tech_name = tech.name.lower()
        for mode in ET:
            mode_name = mode.name.lower()
            for band in tech2band_map[tech]:
                band_name = band.name.lower()
                mipi_map[tech_name][mode_name][band_name]["bw_1p4m"] = \
                mipi_map[tech_name][mode_name][band_name]["bw_5m"]
                mipi_map[tech_name][mode_name][band_name]["bw_3m"] = \
                mipi_map[tech_name][mode_name][band_name]["bw_5m"]
                mipi_map[tech_name][mode_name][band_name]["bw_30m"] = \
                mipi_map[tech_name][mode_name][band_name]["bw_40m"]
                mipi_map[tech_name][mode_name][band_name]["bw_35m"] = \
                mipi_map[tech_name][mode_name][band_name]["bw_40m"]
                mipi_map[tech_name][mode_name][band_name]["bw_45m"] = \
                mipi_map[tech_name][mode_name][band_name]["bw_60m"]
                mipi_map[tech_name][mode_name][band_name]["bw_50m"] = \
                mipi_map[tech_name][mode_name][band_name]["bw_60m"]
                mipi_map[tech_name][mode_name][band_name]["bw_55m"] = \
                mipi_map[tech_name][mode_name][band_name]["bw_60m"]

    # line 550: keep bandwidth string to 1P4M for GSM
    for tech in [TECH.GSM]:
        tech_name = tech.name.lower()
        for mode in ET:
            mode_name = mode.name.lower()
            for band in GSM_BAND:
                band_name = band.name.lower()
                for bw in GSM_BW:
                    bw_name = bw.name.lower()
                    mipi_map[tech_name][mode_name][band_name][bw_name] = \
                    mipi_map[tech_name][mode_name][band_name]["bw_1p4m"]

    # line 643: Determine the set of possible BW settings
    for tech in [TECH.LTE]:
        tech_name = tech.name.lower()
        for mode in [ET.ET]:
            mode_name = mode.name.lower()
            for band in LTE_BAND:
                band_name = band.name.lower()
                for bw in LTE_BW:
                    bw_name = bw.name.lower()
                    for rb in LTE_RB:
                        rb_name = rb.name.lower()
                        next_bw = rb2bw_map[rb]
                        next_bw_name = next_bw.name.lower()
                        mipi_map[tech_name][mode_name][band_name][bw_name][rb_name]["tx_on"] = \
                        mipi_map[tech_name][mode_name][band_name][next_bw_name][rb_name]["tx_on"]

    # Remove Tx_Enable from APT programs
    for tech in TECH:
        tech_name = tech.name.lower()
        for mode in [ET.APT]:
            mode_name = mode.name.lower()
            for band in tech2band_map[tech]:
                band_name = band.name.lower()
                for bw in tech2bw_map[band.__class__]:
                    bw_name = bw.name.lower()
                    for rb in bw2rb_map[bw.__class__]:
                        rb_name = rb.name.lower()
                        mipi_map[tech_name][mode_name][band_name][bw_name][rb_name]["tx_enable"] = []

    # Parameter Independent Scripts
    for k, v in generic_program_keys.items():
        try:
            with open(os.sep.join((scripts_dirname, v + ".csv")), 'rt') as f:
                codes = list(csv.reader(f))
                codes = convert_mipi(codes)
                generic_mipi_map[k] = codes
                del scripts_filenames[scripts_filenames.index(v + ".csv")]
        except FileNotFoundError:
            pass

    # Print the unknown files
    for v in scripts_filenames:
        print("Unknown File: %s", v)

    # Write the config  file
    def hexint_presenter(dumper, data):
        return dumper.represent_int(hex(data))

    yaml.add_representer(int, hexint_presenter)
    with open(config_filename + ".yml", "wt") as f:
        print(config_filename + ".yml")
        yaml.dump(generic_mipi_map, f)
        yaml.dump(mipi_map, f)
    with open(config_filename + ".pkl", "wb") as f:
        print(config_filename + ".pkl")
        pickle.dump(generic_mipi_map, f)
        pickle.dump(mipi_map, f)


def validate_config(config_filename, config_dirname, matlab_dirname):
    # Type: matlab.engine.shareEngine in Matlab before connecting
    import matlab.engine
    from numpy import testing as nptest
    eng = matlab.engine.connect_matlab()

    with open(config_filename + ".pkl", "rb") as f:
        generic_mipi_map = pickle.load(f)
        mipi_map = pickle.load(f)

    for technology in [TECH.LTE]:
        technology_name = technology.name.lower()
        for mode in [ET.APT]:
            mode_name = mode.name.lower()
            for band in LTE_BAND:
                band_name = band.name.lower()
                for bw in LTE_BW:
                    bw_name = bw.name.lower()
                    for rb in LTE_RB:
                        rb_name = rb.name.lower()
                        program = mipi_map[technology_name][mode_name][band_name][bw_name][rb_name]
                        port_name = program["port_name"]
                        if len(port_name) == 0:
                            continue
                        py_codes = generic_mipi_map["power_up"] + generic_mipi_map["wake_up"]\
                                   + program["tx_enable"] + program["tx_on"]
                        with open(os.sep.join((config_dirname, "mipi.csv")), "wt") as f:
                            for code in py_codes:
                                if code[0] == 5:  # Delay
                                    f.write('0x%08x, 0x%08x, %010d\n' % (code[0], code[1], code[2]))
                                else:
                                    f.write('0x%08x, 0x%08x, 0x%08x\n' % (code[0], code[1], code[2]))
                        with open(os.sep.join((matlab_dirname, "mipi_config.csv")), "wt") as f:
                            f.write('%s, %s, %s, %s, %s, nRB%s\n' %
                                    (port_name.upper(), technology_name.upper(), mode_name.upper(),
                                     band_name.upper(), bw_name[3:].upper(), rb_name[3:].upper()))

                        with open(os.sep.join((config_dirname, "mipi.csv")), 'rt') as f:
                            py_codes = np.asarray(list(csv.reader(f)))
                        eng.validate_mipi(nargout=0)
                        with open(os.sep.join((matlab_dirname, "mipi.csv")), 'rt') as f:
                            mat_codes = np.asarray(list(csv.reader(f)))
                        try:
                            nptest.assert_equal(py_codes[:, 2], mat_codes[:, 2])
                        except AssertionError:
                            print("Data Mismatch: %s_%s_%s_%s_%s" % (technology_name, mode_name, band_name, bw_name, rb_name))
                        try:
                            nptest.assert_equal(py_codes[:, 1], mat_codes[:, 1])
                        except AssertionError:
                            print("Address Mismatch: %s_%s_%s_%s_%s" % (technology_name, mode_name, band_name, bw_name, rb_name))
                        try:
                            nptest.assert_equal(py_codes[:, 0], mat_codes[:, 0])
                        except AssertionError:
                            pass
                            # print("Write Type Mismatch: %s_%s_%s_%s_%s" % (technology_name, mode_name, band_name, bw_name, rb_name))


if __name__ == "__main__":
    script_dirname = r"C:\ETTS_TCF\rffe-scripts\modulator\QET5100\1.0"
    config_dirname = os.sep.join((Settings().data_root, "config", "device", "dut", "mipi", "et", "qualcomm"))
    tx_enable_filename = os.sep.join((config_dirname, "tx_enable.csv"))
    tx_on_filename = os.sep.join((config_dirname, "tx_on.csv"))
    config_filename = os.sep.join((config_dirname, "qet5100_3"))
    matlab_dirname = r"C:\ETTS_TCF"
    # create_config(script_dirname, tx_enable_filename, tx_on_filename, config_filename)
    validate_config(config_filename, config_dirname, matlab_dirname)
