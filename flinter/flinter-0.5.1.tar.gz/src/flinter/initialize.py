"""Module containing base functions to lint
    and dectect broken formatting rules
"""
import re
import os
import pkg_resources
import yaml
import shutil
import warnings


__all__ = ["rate", "new_rules", "init_format_rules"]

def rate(lines_nb, struct_nb, regexp_nb):
    """rate the quality of each record"""
    if lines_nb == 0:
        rate= 0
    else:
        rate = (float(struct_nb * 5 + regexp_nb) / lines_nb) * 10
        rate = 10.0 - rate
    return rate

def new_rules(filename=None):
    """Create default rules file."""
    if filename is None:
        filename = "./flinter_rc.yml"
    write = True
    if os.path.isfile(filename):
        msg = f'File {filename} already exists. Overwrite ? [y/N] '
        if input(msg).lower() == 'n':
            write = False
    if write:
        print(f'Generating rule file {filename} for Flinter.')
        shutil.copy2(
            pkg_resources.resource_filename("flinter", "fortran_rc_default.yml"),
            filename,
        )


class RuleSets:
    def __init__(self):
        self.sets = []

    def add(self, rules):
        self.sets.insert(0, rules)

    def get_from_ext(self, ext):
        for rules in self.sets:
            if re.fullmatch(rules["extension"], ext, re.I):
                return rules
        return None

    def get_from_fname(self, fname):
        return self.get_from_ext(os.path.splitext(fname)[-1][1:])


def init_languages_specs(user_rc_list=None):
    """Load format rules from resosurces.
    """
    rule_sets = RuleSets()
    for default_rc in ["fortran_rc_default.yml", "python_rc_default.yml", "cpp_rc_default.yml"]:
        default_rc = pkg_resources.resource_filename("flinter", default_rc)
        rule_sets.add(init_format_rules(default_rc))

    if user_rc_list:
        for user_rc in user_rc_list:
            rule_sets.add(init_format_rules(user_rc))

    return rule_sets

def init_format_rules(flinter_rc):
    with open(flinter_rc) as fin:
        rules = yaml.load(fin, Loader=yaml.FullLoader)
    extension = rules.get("extension", r"f\d\d")

    # create syntax reference 
    syntax = rules.get("fortran-syntax") or rules["syntax"]
    if "fortran-syntax" in rules:
        warnings.warn("Deprecated use of \"fortran-syntax\" , use the more generic \"syntax\" qualifier")
    if "extension" not in rules:
        warnings.warn("Rule file with no extension field default to fortran, prefer explicitely specifying one")
    if "namespace_blocks" not in syntax or "context_blocks" not in syntax:
        if "blocks" in syntax:
            warnings.warn("Deprecated use of \"blocks\" in syntax, use instead \"namespace_blocks\" and \"context_blocks\"")
        else:
            warnings.warn("\"namespace_blocks\" and \"context_blocks\" are not defined in the syntax")
        syntax["namespace_blocks"] = ["program", "module"]
        syntax["context_blocks"] = ["subroutine", "function"]
    else:
        syntax["blocks"] = syntax.get("blocks", [])+syntax["namespace_blocks"]+syntax["context_blocks"]
    syntax.setdefault("ignore_blocks", [])

    # create syntax copy for regular expression replacement
    syntax_re = dict()
    for key, value in syntax.items():
        syntax_re[key] = r"|".join(value).lower()
        syntax_re[key+"_upper"] = syntax_re[key].upper()

    # select active rules
    # compile the rules
    regexp_rules = dict()
    default_rule = {
        "replacement": None,
        "active": True,
        "include-comments": False,
        "case-sensitive": False,
    }
    for name, rule in rules["regexp-rules"].items():
        for key, value in default_rule.items():
            rule.setdefault(key, value)
        if rule["active"]:
            regexp_rules[name] = _compile_format_rule(rule, syntax_re)

    struct_rules = rules["structure-rules"]
    if "var-declaration" not in struct_rules:
        warnings.warn("\"var-declaration\" is not defined in the rules")
        struct_rules["var-declaration"] = r"(?:{types}|{types_upper})\s*(?:\(.*\))?\s*(?:::| )\s*(\w+(?:\s*,\s*\w+)*)"
    for key, value in struct_rules.items():
        if isinstance(value, str):
            struct_rules[key] = re.compile(value.format(**syntax_re), re.I)
    
    out= {
        "syntax": syntax,
        "regexp-rules": regexp_rules,
        "struct-rules": struct_rules,
        "extension": extension,
        "name": os.path.split(flinter_rc)[-1]
    }

    return out

def _compile_format_rule(rule, syntax):
    """Compile the regexp action for a rule
    :param rule: dict
        - message
        - regexp
        - replacement
        the rules to be implemented
        some rules a based upon lists stored in syntax
    :param syntax: dict
        - types
        - operators
        - structs
        - punctuation
        language specific lists of items

    """
    if rule["message"] is not None:
        rule["message"] = rule["message"].format(**syntax)
    else:
        rule["message"] = None
    
    flags = 0
    if not rule["case-sensitive"]:
        flags |= re.I
    rule["regexp"] = re.compile(rule["regexp"].format(**syntax), flags)

    return rule