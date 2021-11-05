# -*- coding: utf-8 -*-
"""Pygments Style: mrtools.

.. moduleauthor:: Michael Rippstein <michael@anatas.ch>


"""

from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, \
     Number, Operator, Generic, Whitespace, Punctuation, Other, Literal

NORD_COLORS = {
    # Polar Night
    'night00': '#2e3440',
    'night01': '#3d4454',
    'night02': '#4b5569',
    'night03': '#5a667d',
    # Snow Storm
    'storm00': '#b0bac5',
    'storm01': '#d3d9e3',
    'storm02': '#dde2eb',
    'storm03': '#e6ebf2',
    # Frost
    'frost00': '#8fbcbb',
    'frost01': '#88c0d0',
    'frost02': '#81a1c1',
    'frost03': '#5e81ac',
    # Aurora
    'aurora1': '#bf616a',  # red
    'aurora2': '#d08770',  # orange
    'aurora3': '#ebcb8b',  # yellow
    'aurora4': '#a3be8c',  # green
    'aurora5': '#b48ead',  # violett
}


class MrToolsStyle(Style):    # pylint: disable=too-few-public-methods
    """Pygments Style for the Sphinx Theme `mrtools`."""

    # work in progress...

    colors = NORD_COLORS

    background_color = colors['night01']
    highlight_color = colors['night03']
    default_style = colors['night03']

    styles = {
        # No corresponding class for the following:
        # Text:                 "", # class:  ''
        Whitespace:             "underline " + colors['storm03'],       # class: 'w'
        Error:                  colors['aurora1'] + " border:" + colors['aurora2'],  # class: 'err'
        Other:                  colors['storm03'],              # class 'x'

        Comment:                "italic " + colors['storm00'],  # class: 'c'
        Comment.Multiline:      "italic " + colors['storm00'],  # class: 'cm'
        Comment.Preproc:        "italic " + colors['storm00'],  # class: 'cp'
        Comment.Single:         "italic " + colors['storm00'],  # class: 'c1'
        Comment.Special:        "italic " + colors['storm00'],  # class: 'cs'

        Keyword:                "bold " + colors['frost00'],    # class: 'k'
        Keyword.Constant:       "bold " + colors['frost00'],    # class: 'kc'
        Keyword.Declaration:    "bold " + colors['frost00'],    # class: 'kd'
        Keyword.Namespace:      "bold " + colors['frost00'],    # class: 'kn'
        Keyword.Pseudo:         "bold " + colors['frost00'],    # class: 'kp'
        Keyword.Reserved:       "bold " + colors['frost00'],    # class: 'kr'
        Keyword.Type:           "bold " + colors['frost00'],    # class: 'kt'

        Operator:               'bold ' + colors['frost00'],    # class: 'o'
        Operator.Word:          'bold ' + colors['frost00'],    # class: 'ow'

        Punctuation:            "bold " + colors['storm03'],    # class: 'p'

        # because special names such as Name.Class, Name.Function, etc.
        # are not recognized as such later in the parsing, we choose them
        # to look the same as ordinary variables.
        Name:                   colors['storm03'],              # class: 'n'
        Name.Attribute:         colors['storm03'],              # class: 'na'
        Name.Builtin:           colors['aurora2'],              # class: 'nb'
        Name.Builtin.Pseudo:    colors['aurora2'],              # class: 'bp'
        Name.Class:             colors['storm03'],              # class: 'nc'
        Name.Constant:          colors['storm03'],              # class: 'no'
        Name.Decorator:         "bold " + colors['storm01'],    # class: 'nd'
        Name.Entity:            colors['storm03'],              # class: 'ni'
        Name.Exception:         "bold " + colors['aurora1'],    # class: 'ne'
        Name.Function:          colors['storm03'],              # class: 'nf'
        Name.Property:          colors['storm03'],              # class: 'py'
        Name.Label:             colors['storm03'],              # class: 'nl'
        Name.Namespace:         colors['storm03'],              # class: 'nn'
        Name.Other:             colors['storm03'],              # class: 'nx'
        Name.Tag:               colors['storm03'],              # class: 'nt'
        Name.Variable:          colors['storm03'],              # class: 'nv'
        Name.Variable.Class:    colors['storm03'],              # class: 'vc'
        Name.Variable.Global:   colors['storm03'],              # class: 'vg'
        Name.Variable.Instance: colors['storm03'],              # class: 'vi'

        Number:                 colors['storm03'],              # class: 'm'
        Number.Float:           colors['storm03'],              # class: 'mf'
        Number.Hex:             colors['storm03'],              # class: 'mh'
        Number.Integer:         colors['storm03'],              # class: 'mi'
        Number.Integer.Long:    colors['storm03'],              # class: 'il'
        Number.Oct:             colors['storm03'],              # class: 'mo'

        Literal:                colors['storm03'],              # class: 'l'
        Literal.Date:           colors['storm03'],              # class: 'ld'

        String:                 colors['aurora4'],              # class: 's'
        String.Backtick:        colors['aurora4'],              # class: 'sb'
        String.Char:            colors['aurora4'],              # class: 'sc'
        String.Doc:             "italic " + colors['frost02'],  # class: 'sd'
        String.Double:          colors['aurora4'],              # class: 's2'
        String.Escape:          colors['aurora4'],              # class: 'se'
        String.Heredoc:         colors['aurora4'],              # class: 'sh'
        String.Interpol:        colors['aurora4'],              # class: 'si'
        String.Other:           colors['aurora4'],              # class: 'sx'
        String.Regex:           colors['aurora4'],              # class: 'sr'
        String.Single:          colors['aurora4'],              # class: 's1'
        String.Symbol:          colors['aurora4'],              # class: 'ss'

        Generic:                colors['storm03'],              # class: 'g'
        Generic.Deleted:        colors['night02'],              # class: 'gd'
        Generic.Emph:           "italic " + colors['storm03'],  # class: 'ge'
        Generic.Error:          colors['aurora1'],              # class: 'gr'
        Generic.Heading:        "bold " + colors['storm03'],    # class: 'gh'
        Generic.Inserted:       colors['storm03'],              # class: 'gi'
        Generic.Output:         "italic " + colors['storm03'],  # class: 'go'
        Generic.Prompt:         colors['storm03'],              # class: 'gp'
        Generic.Strong:         "bold " + colors['storm03'],    # class: 'gs'
        Generic.Subheading:     "bold " + colors['storm03'],    # class: 'gu'
        Generic.Traceback:      "bold " + colors['storm01'],    # class: 'gt'
    }
