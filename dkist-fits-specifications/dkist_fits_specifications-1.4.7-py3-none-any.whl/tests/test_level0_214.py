from dkist_fits_specifications.spec214.level0 import (
    load_level0_spec214,
    spec214_122_key_map,
)


def test_key_map():
    key_map = spec214_122_key_map()
    assert key_map["LINEWAV"] == "WAVELNTH"


def test_level0_spec():
    spec = load_level0_spec214()
    assert "WAVELNTH" in spec["fits"]
    assert spec["dataset"]["LINEWAV"]["rename"] == "WAVELNTH"

    assert "VSPNUMST" in spec["visp"]
    assert "VSPSTNUM" in spec["visp"]
    assert "IPTASK" in spec["dkist-op"]
