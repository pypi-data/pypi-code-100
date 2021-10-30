#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#    Wisteria Copyright (C) 2021 suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of Wisteria.
#    Wisteria is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Wisteria is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Wisteria.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
    Wisteria project : wisteria/reprfmt.py

    Format some objects representation by adding some text attributes.

    ___________________________________________________________________________

    o  fmt_boolsuccess(bool_success)
    o  fmt_data(data_objectname)
    o  fmt_error(msg)
    o  fmt_list(listitems)
    o  fmt_mem_usage(bytesnumber)
    o  fmt_nodata(string)
    o  fmt_nounplural(string, number)
    o  fmt_percentage(percentage)
    o  fmt_projectversion(add_timestamp=False)
    o  fmt_ratio(inttotal_and_floatratio)
    o  fmt_serializer0(serializer_name)
    o  fmt_serializer(serializer_name)
    o  fmt_stringlength(int_stringlength)
    o  fmt_time(floattime)
    o  fmt_title(title)

    o  fmt_exaequowith(item, listitems, func=fmt_serializer,
                          prefix=", [i]ex aequo[/i] with ")
    o  fmt_exaequowith_hall(results, item_number, attribute, func=fmt_serializer,
                               prefix=", [i]ex aequo[/i] with ")
"""
import datetime
import re

from wisteria.aboutproject import __version__, __projectname__
import wisteria.globs


def fmt_boolsuccess(bool_success):
    """
        fmt_boolsuccess()

        Format the input argument into a string. The input argument is a (bool)success.
            ex: False > "NOT OK"

        _______________________________________________________________

        ARGUMENT: (bool)bool_success

        RETURNED VALUE: a formatted string representing the (bool)bool_success.
    """
    if bool_success is None:
        return fmt_nodata()
    return "ok" if bool_success else "[red]NOT OK[/red]"


def fmt_data(data_objectname):
    """
        fmt_data()

        Format the representation of (str)data_objectname.

        _______________________________________________________________________

        ARGUMENT: (str)data_objectname

        RETURNED VALUE: (str)data_objectname + some text attributes.
    """
    return f"[bold white]{data_objectname}[/bold white]"


def fmt_error(msg):
    """
        fmt_error()

        Format the representation of (str)msg

        _______________________________________________________________________

        ARGUMENT: (str)msg

        RETURNED VALUE: (str)msg + some text attributes.
    """
    return re.sub(r"\(ERRORID[\d]+\)",
                  lambda re_match: f"[bold red]{re_match.group()}[/bold red]",
                  msg)


def fmt_list(listitems, func=None):
    """
        fmt_list()

        Return a (str)list of words written in good English, something
        like "a, b, and c" (no Oxford Comma here, confer
        https://www.grammar-monster.com/lessons/commas_the_Oxford_comma.htm)

        If <func> is not None, apply <func> to each item in <listitems>.

        _______________________________________________________________________

        ARGUMENTS:
        o  (list of str)listitems
        o  (callable)   func, the function to be applied to each item in
                        the result.

        RETURNED VALUE: (str)a formatted string with all items in <listitems>.
    """
    if len(listitems) == 0:
        return ""
    if len(listitems) == 1:
        return listitems[0] if not func else func(listitems[0])
    if len(listitems) == 2:
        return f"{func(listitems[0])} and {func(listitems[1])}"
    return f"{', '.join(func(listitem) for listitem in listitems[:-1])} and {func(listitems[-1])}"


def fmt_mem_usage(bytesnumber):
    """
        fmt_mem_usage()

        Format the representation of (int)bytesnumber.

        _______________________________________________________________________

        ARGUMENT: (int)bytesnumber

        RETURNED VALUE: (str)bytesnumber + some text attributes.
    """
    if bytesnumber is None:
        return fmt_nodata()
    if bytesnumber == 0:
        return "0 byte"
    if bytesnumber < 120000:
        return f"{bytesnumber} bytes"
    if bytesnumber < 120000000:
        return f"{bytesnumber/1000:.1f} Ko"
    if bytesnumber < 120000000000:
        return f"{bytesnumber/1000000:.1f} Mo"
    if bytesnumber < 120000000000000:
        return f"{bytesnumber/1000000000:.1f} Go"
    return f"{bytesnumber/1000000000000:.1f} Po"


def fmt_nodata(string=None):
    """
        fmt_nodata()

        Return a string with rich text attribute saying that no data is available.

        _______________________________________________________________________

        ARGUMENT:(None or str)if string is None, a default string ("no data")
                 will be used; if string is a str, this string will be used.

        RETURNED VALUE: (str)"no data" string + some text attributes.
    """
    if not string:
        string = "(no data)"

    return f"[red]{string}[/red]"


def fmt_nounplural(string,
                   number):
    """
        fmt_nounplural()

        Return string with a final -s if <number> is greater than one.

        _______________________________________________________________________

        o  (str)string, a string ending with a word to which a final s may be added
        o  (int)number, 0 <= number

        RETURNED VALUE: (str)string + -s if <number> is greater than one.
    """
    if number <= 1:
        return string
    return string+"s"


def fmt_percentage(percentage):
    """
        fmt_percentage()

        Format the representation of (float)percentage.

        _______________________________________________________________________

        ARGUMENT: (float)percentage

        RETURNED VALUE: (str)percentage + some text attributes.
    """
    return f"{percentage:.2f}%"


def fmt_projectversion(add_timestamp=False):
    """
        fmt_ratio()

        Format __projectname__, __version__ into a string.
        If timestamp is True, add the current timestamp.

        PLEASE DO NOT ADD RICH ATTRIBUTES TO THE RETURNED STRING
        since this function is called by wisteria.py with a simple
        print() statement.

        _______________________________________________________________

        ARGUMENT: (bool)add_timestamp, if True, add the current timestamp
                  to the returned string.

        RETURNED VALUE: a formatted string with __projectname__, __version__
                        and (if timestamp is True) the current timestamp.
    """
    if add_timestamp:
        return f"{__projectname__}, {__version__} ({str(datetime.datetime.now())})"
    return f"{__projectname__}, {__version__}                                 "


def fmt_ratio(inttotal_and_floatratio):
    """
        fmt_ratio()

        Format the input argument into a string. The input argument is an absolute
        (int)number and a (float)fraction, its ratio.
            ex: (3, 0.5) > "3 (50 %)"

        _______________________________________________________________

        ARGUMENT: (None|(int, float))inttotal_and_floatratio

        RETURNED VALUE: a formatted string representing the input argument.
    """
    if inttotal_and_floatratio != (None, None):
        return f"{inttotal_and_floatratio[0]} " \
            f"({fmt_percentage(100*inttotal_and_floatratio[1])})"
    return fmt_nodata()


def fmt_serializer0(serializer_name):
    """
        fmt_serializer0()

        Format the representation of (str)serializer_name.

        _______________________________________________________________________

        ARGUMENT: (str)serializer_name

        RETURNED VALUE: (str)serializer_name + some text attributes.
    """
    return "[yellow]" \
        f"{serializer_name}" \
        "[/yellow]"


def fmt_serializer(serializer_name):
    """
        fmt_serializer()

        Format the representation of (str)serializer_name; if possible, replace it by its
        .human_name.

        _______________________________________________________________________

        ARGUMENT: (str)serializer_name

        RETURNED VALUE: (str)serializer_name + some text attributes.
    """
    if serializer_name in wisteria.globs.SERIALIZERS:
        return f"{fmt_serializer0(wisteria.globs.SERIALIZERS[serializer_name].human_name)}"
    return f"{fmt_serializer0(serializer_name)}"


def fmt_stringlength(int_stringlength):
    """
        fmt_stringlength()

        Format the input argument into a string. The input argument is a (int)number
        of characters
            ex: 3 > "3 chars"

        Please note that the unit has deliberately not been added to the end of the string.
        _______________________________________________________________

        ARGUMENT: (None|int)int_stringlength, a string number.

        RETURNED VALUE: a formatted string representing the input argument.
    """
    if int_stringlength is None:
        return fmt_nodata()
    return f"{int_stringlength}"


def fmt_time(floattime):
    """
        fmt_time()

        Format the input argument into a string. The input argument is a (float)time laps.
            ex: 0.333345677 > "0.333345"

        Please note that the unit has deliberately not been added to the end of the string.
        _______________________________________________________________

        ARGUMENT: (None|float)floattime

        RETURNED VALUE: a formatted string representing the input argument.
    """
    if floattime is None:
        return fmt_nodata()
    return f"{floattime:.6f}"


def fmt_title(title):
    """
        fmt_title()

        Format the representation of (str)title.

        _______________________________________________________________________

        ARGUMENT: (str)title

        RETURNED VALUE: (str)title + some text attributes.
    """
    return f"[bold white on blue]{title}[/bold white on blue]"


# function defined here since it depends from fmt_list().
def fmt_exaequowith(item,
                    listitems,
                    func=fmt_serializer,
                    prefix=", [i]ex aequo[/i] with "):
    """
        fmt_exaequowith()

        Return a list of the items in <listitems> without <item>.

        <listitems> is a list of (str)items, <item> being one of the items
        something like:
                listitems=['a', 'b', 'c'], items="b".
        This function will return:
                <prefix>(~"ex aequo") + "a and c".

        _______________________________________________________________________

        ARGUMENTS:
        o  (str)           item
        o  (list of str)   listitems
        o  (callable)      func        , callable that will be called upon each <item>.
        o  (str)           prefix      , string that will be added before the result

        RETURNED VALUE: (str)
    """
    if len(listitems) == 1:
        return ""
    listitems.remove(item)
    return prefix + fmt_list(listitems, func)


def fmt_exaequowith_hall(results,
                         item_number,
                         attribute,
                         func=fmt_serializer,
                         prefix=", [i]ex aequo[/i] with "):
    """
        fmt_exaequowith_hall()

        See fmt_exaequowith(): this function returns all serializers
        whose score is equal to results.hall[attribute][item_number][0];
        the returned list doesn't contain results.hall[attribute][item_number][1]

        By example, if all serializers whose score is 15 are ['a', 'b', 'c']
        and if results.hall[attribute][item_number][1]=="a", the returned
        string will be:
                <prefix>(~"ex aequo") + "a and c".


        _______________________________________________________________________

        ARGUMENTS:

        o  (SerializationResults) results     : object where .hall is stored
        o  (int)                  item_number : in order to work on
                                                        results.hall[attribute][item_number]
        o  (str)                  attribute   : in order to work on
                                                        results.hall[attribute][item_number]
        o  (callable)             func        , callable that will be called upon each <item>.
        o  (str)                  prefix      , string that will be added before the result

        RETURNED VALUE: (str)
    """
    score, serializer = results.hall[attribute][item_number]
    listitems = [_serializer for _score, _serializer in results.hall[attribute] if _score == score]
    if len(listitems) == 1:
        return ""
    listitems.remove(serializer)
    return prefix + fmt_list(listitems, func)
