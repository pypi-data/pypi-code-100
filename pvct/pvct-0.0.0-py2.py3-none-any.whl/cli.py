"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mpvct` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``pvct.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``pvct.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""

from glob import glob  # for command line arguments
import sys  # for command line arguments
from pvct import PVCT
from gooey import Gooey, GooeyParser
import argparse


# from argparse_formatter import ParagraphFormatter


# https://stackoverflow.com/a/26986546/36061
# work around to this bug: https://bugs.python.org/issue9338
class Formatter(argparse.HelpFormatter):
    # use defined argument order to display usage
    def _format_usage(self, usage, actions, groups, prefix):
        if prefix is None:
            prefix = 'usage: '

        # if usage is specified, use that
        if usage is not None:
            usage = usage % dict(prog=self._prog)

        # if no optionals or positionals are available, usage is just prog
        elif usage is None and not actions:
            usage = '%(prog)s' % dict(prog=self._prog)
        elif usage is None:
            prog = '%(prog)s' % dict(prog=self._prog)
            # build full usage string
            action_usage = self._format_actions_usage(actions, groups)  # NEW
            usage = ' '.join([s for s in [prog, action_usage] if s])
            # omit the long line wrapping code
        # prefix with 'usage:'
        return '%s%s\n\n' % (prefix, usage)


HELP = \
    """
    This program is used to create a pVCT diffraction pattern from many FCT diffraction patterns.\n
    usage: >python PVCT.pyz lam mono B abs formula min max [filenames... | D]\n
    If you provide filenames, it will use those to creat a pVCT pattern, if not, it will run a simulation.\n
    lam: (float) wavelength in A or energy in keV.
    mono: (float) monochromator angle in deg 2Th (0 for none, 90 for synchrotron).
    B: (float) average temperature factor (0.5 is a good start).
    abs: (float) capillary absorption in mu*R or incident angle for fixed-incident-beam. (0 for no correction).
    formula: (string) Chemical formula --> \"La 1 B 6\" of \"Fe 1\".
    min: (float) angle of first peak in deg 2Th.
    max: (float) maximum angle in deg 2Th.
    filenames: (string) list of file names - XY or XYE format. Wildcards accepted eg *.xy, la?.xy
    D: (int) number of diffraction patterns to simulate.\n
    Read the paper for more information.
    """

CITATION = "Rowles, M.R., (2021) 'PVCT: A program for constructing pseudo-variable-count-time diffraction patterns', https://github.com/rowlesmr/pvct"

# If program is run with command line arguments, assume you don't want the GUI.
# https://github.com/chriskiehl/Gooey/issues/449
if len(sys.argv) >= 2:
    if "--ignore-gooey" not in sys.argv:
        sys.argv.append("--ignore-gooey")


# https://stackoverflow.com/a/27008413/36061
# argparse.ArgumentParser  GooeyParser
parser = GooeyParser(description="This program is used to create a pVCT diffraction pattern from many FCT diffraction patterns.",
                     epilog="If this is useful, please cite: " + CITATION, formatter_class=Formatter)

parser.add_argument("lam", type=float, help="Wavelength in A or energy in keV")
parser.add_argument("mono", type=float, help="Monochromator angle in deg 2Th (0 for none, 90 for synchrotron)")
parser.add_argument("B", type=float, help="Average temperature factor (0.5 is a good start)")
parser.add_argument("abs", type=float, help="Capillary absorption in mu*R or incident angle for fixed-incident-beam. (0 for no correction)")
parser.add_argument("formula", type=str, help="Chemical formula as a string --> 'La 1 B 6' of 'Fe 1'")
parser.add_argument("min", type=float, help="Angle of first peak in deg 2Th")
parser.add_argument("max", type=float, help="Maximum angle in deg 2Th")

group = parser.add_mutually_exclusive_group(required=True)

group.add_argument("-D", help="Number of diffraction patterns to simulate.", type=int) #, dest="val")
group.add_argument('-f', '--filename',
                   nargs='+',
                   help="Names of FCT diffraction files to convert to pVCT format. Wildcards accepted.",
                   widget="MultiFileChooser",
                   gooey_options={
                       'wildcard':
                           "XY files (*.xy)|*.xy|"
                           "XYE files (*.xye)|*.xye|"
                           "All files (*.*)|*.*"}
                   )


@Gooey(terminal_font_family='Courier New',
       program_name="PVCT",
       default_size=(600, 860))
def main(args=None):
    args = parser.parse_args(args=args)

    lam = args.lam
    mono = args.mono
    B = args.B
    abs_ = args.abs
    formula = args.formula
    min_ = args.min
    max_ = args.max

    p = PVCT(lam, mono, B, abs_, formula, min_, max_)

    # split between the two different options - simulate or calculate
    if args.D is not None:
        D = args.D
        p.simulate(D)
        p.calc_sum_array()
    else:
        filenames = []
        for file in args.filename:
            filenames += glob(file)
        p.read_filenames(filenames)
        p.calc_sum_array()
        p.combine_files()
        p.writeToFile()
        p.writeSumToFile()


if __name__ == "__main__":
    main()
