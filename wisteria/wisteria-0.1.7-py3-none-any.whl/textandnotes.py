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
    Wisteria project : wisteria/textandnotes.py

    With the TextAndNotes class, add bunch of text that may contains notes;
    these notes are added with a special syntax (__note:XXXXX__) and are
    automatically numbered and added at the end of the final text.

    ___________________________________________________________________________

    o  TextAndNotes class
"""
import re

from wisteria.wisteriaerror import WisteriaError


class TextAndNotes(list):
    """
        TextAndNotes class

        With the TextAndNotes class, add bunch of text that may contains notes;
        these notes are added with a special syntax (__note:XXXXX__) and are
        automatically numbered and added at the end of the final text.

        By example:
                txt = TextAndNotes()
                txt.append("First line with a note (__note:myfirstnote__)")
                txt.notes.append(("__note:myfirstnote__",
                                  "This is a footnote about first line."))

                txt.output() will produce:
                        "First line with a note(¹)"
                        ""
                        "(¹) This is a footnote about first line."

        _______________________________________________________________________

        class attributes:

        o  notesregex   : (re.Match)regex to find the notes in the text

        instance attributes:

        o  (int)next_notessymbols: (str)number of the next note
        o  (list of str)notes    : notes to be added to the text

        methods:

        o  __init__(self)
        o  delete_duplicated_notes(self)
        o  next_notessymbol(self)
        o  output(self)
    """
    notesregex = re.compile(r'__note\:(?P<notename>[a-z_]+)__')

    def __init__(self):
        """
            TextAndNotes.__init__()
        """
        list.__init__(self)
        self.next_notessymbols = 1  # what will be the next notes symbols index ?
        self.notes = []

    def delete_duplicated_notes(self):
        """
            TextAndNotes.delete_duplicated_notes()

            Modify .notes in place and remove from it duplicate items.
        """
        self.notes = list(dict.fromkeys(self.notes))

    def next_notessymbol(self):
        """
            TextAndNotes.next_notessymbol()

            Return the string representing the next note (that is, '¹', '²', '³', ...)

            ___________________________________________________________________

            RETURNED VALUE: (str)a string like '¹', '²', '³', ...
        """
        res = str(self.next_notessymbols)
        res = res.replace('0', '⁰')
        res = res.replace('1', '¹')
        res = res.replace('2', '²')
        res = res.replace('3', '³')
        res = res.replace('4', '⁴')
        res = res.replace('5', '⁵')
        res = res.replace('6', '⁶')
        res = res.replace('7', '⁷')
        res = res.replace('8', '⁸')
        res = res.replace('9', '⁹')

        self.next_notessymbols += 1

        return res

    def output(self):
        """
            TextAndNotes.output()

            Return the text and the notes with the expected formatting.

            ___________________________________________________________________

            RETURNED VALUE: (str)the text and the notes with the expected formatting.
        """
        def fullnotename2symbol(match):
            """
                Replace the full note name (__note:XXX__) by its symbol
                e.g. "(__note:overallscore__)" > (¹)

                _______________________________________________________________

                ARGUMENT: (re.Match)match, a full note like __note:mynote__

                RETURNED VALUE: (str)the note with its symbolic name, like '¹'.
            """
            return notes2notessymbols[match.group('notename')]

        res = []
        notes2notessymbols = {}

        self.delete_duplicated_notes()

        for line in self:
            for match in re.finditer(TextAndNotes.notesregex, line):
                if match.group('notename') not in notes2notessymbols:
                    notes2notessymbols[match.group('notename')] = self.next_notessymbol()
                line = re.sub(TextAndNotes.notesregex,
                              fullnotename2symbol,
                              line)
            res.append(line)

        if self.notes:
            res.append("\n\n- notes -")

            for fullnotename, note in self.notes:
                if fullnotename not in notes2notessymbols:
                    raise WisteriaError(
                        "Ill-formed TextAndNotes object: "
                        f"unknown note name '{fullnotename}' read in note '{note}'; "
                        f"defined notes are {tuple(notes2notessymbols.keys())} .")
                note_symbol = notes2notessymbols[fullnotename]
                res.append(f"\n[{note_symbol}] {note}")

        return "".join(res)
