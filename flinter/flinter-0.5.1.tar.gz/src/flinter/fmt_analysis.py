"""
Format analysis module.
=======================

This will use the regexp rules given in configuration file to identify errors.
It intends to follows the coding conventions
mentioned in
`OMS Documentation Wiki page <https://alm.engr.colostate.edu/cb/wiki/16983>`__

The repalcement pipeline exists but is not implemented fully,
since I am not so sure of the result for multiple errors in one line.

"""


__all__ = ["fmt_analysis"]


TAB_WIDTH = 8


def fmt_analysis(lines, lines_with_comments, start_line, rules, verbose=False):
    """Start the linter of file FILENAME."""
    all_errors = dict()
    
    for i, (line, line_with_comments) in enumerate(zip(lines, lines_with_comments), start_line):
        errors_found = parse_format_line(line, line_with_comments, i, rules, verbose)

        for key, value in errors_found.items():
            nb_ = len(value)
            if key in all_errors:
                all_errors[key] += nb_
            else:
                all_errors[key] = nb_

    broken_rules = dict()
    for key in all_errors:
        #broken_rules[format_rules[key]["message"]] = all_errors[key]
        broken_rules[key] = all_errors[key]

    return broken_rules

def parse_format_line(line, line_with_comments, line_no, rules, verbose):
    """Analyse line

    :param line: str, line itself
    :param line_no: int, position in the file
    :param rules: rules read from config

    :returns :
        dict {
            rule_name : nb_of_error
        )
         """
    msg_info = {"line_no": line_no, "line": line_with_comments}
    out = dict()
    for key, rule in rules.items():
        error_nb = _parse_format_rule(
            line_with_comments if rule["include-comments"] else line,
            msg_info, rule, verbose=verbose)
        if error_nb > 0:
            try:
                out[key].append(msg_info)
            except KeyError:
                out[key] = [msg_info]

    return out


def _parse_format_rule(line, msg_info, rule, verbose):
    """Interpret rules

    :param line: str, line to check
    :param msg_info: dict, identifier of position
    :param rule: key to the rules dictionnary

    return:
        dict
        errors: number of errors
        modifs: number of mofifs
    """
    error_nb = 0
    #modifs_nb = 0
    #replacement = line
    for res in rule["regexp"].finditer(line):
        msg_info["column"] = _true_position(res.start(), msg_info["line"])
        msg_info["span"] = _true_position(res.end(), msg_info["line"])-msg_info["column"]
        # if rule["replacement"] is not None:
        #     modifs_nb += 1
        #     replacement = rule["regexp"].sub(rule["replacement"], replacement)
        # msg_info["replacement"] = replacement
        #if rule["message"] is not None:
        error_nb += 1
        if verbose:
            print(_str_msg(rule["message"], msg_info, line))
    #        print("|" + replacement)

    return error_nb

def _true_position(pos, line):
    return len(line[:pos].expandtabs(TAB_WIDTH))

def _str_msg(msg, info, line):
    """Format error message.

    :param msg: category of message
    :param info: dict locating the error."""
    return f"""\
{info["line_no"]}:{info["column"]}: {msg}:
|{info["line"].expandtabs(TAB_WIDTH)}
|{" " * info["column"] + "^" + "~" * (info["span"]-1)}"""