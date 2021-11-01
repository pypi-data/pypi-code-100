import yaml
import pkgutil

_color_rules_settings = yaml.safe_load(
    pkgutil.get_data(
        __name__,
        "defaults/color_rules.yaml"))

settings = yaml.safe_load(
    pkgutil.get_data(
        __name__,
        "defaults/settings.yaml"))
settings.update(_color_rules_settings)