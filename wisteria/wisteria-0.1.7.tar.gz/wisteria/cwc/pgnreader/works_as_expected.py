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
    Wisteria project : wisteria/cwc/pgnreader/works_as_expected.py

    initialize() and works_as_expected() functions for all cwc/pgnreader/ classes.


    ___________________________________________________________________________

    o  initialize(obj)
    o  works_as_expected(obj)
"""
from wisteria.dmfile import DMFile


def initialize(obj):
    """
        initialize() function
    """
    data = """
[Event "Aimchess US Rapid Prelim"]
[Site "chess24.com INT"]
[Date "2021.08.29"]
[Round "6.6"]
[White "Dominguez Perez, Leinier"]
[Black "Aronian, Levon"]
[Result "0-1"]
[WhiteTitle "GM"]
[BlackTitle "GM"]
[WhiteElo "2758"]
[BlackElo "2782"]
[ECO "C53"]
[Opening "Giuoco Piano"]
[WhiteFideId "3503240"]
[BlackFideId "13300474"]
[EventDate "2021.08.28"]

1. e4 e5 2. Nf3 Nc6 3. Bc4 Bc5 4. c3 Nf6 5. d3 O-O 6. O-O d5 7. exd5 Nxd5 8. Re1
Bg4 9. Nbd2 Nb6 10. h3 Bh5 11. Bb3 Qxd3 12. Nxe5 Qf5 13. Nef3 Rad8 14. Qe2 Nd5
15. Ne4 Bxf3 16. Qxf3 Qxf3 17. gxf3 Bb6 18. a4 h6 19. Rd1 Nde7 20. Rxd8 Rxd8 21.
Kf1 Kf8 22. Be3 Nf5 23. Bxb6 axb6 24. Rd1 Rxd1+ 25. Bxd1 Ne5 26. Ng3 Nh4 27. Ke2
Nhxf3 28. Ke3 Ng1 29. b3 Nxh3 30. f4 Ng6 31. Nh5 Ne7 32. Bg4 Nd5+ 33. Kf3 g6 34.
Bxh3 gxh5 35. Bc8 Nxc3 36. Bxb7 Ke7 37. Ke3 Kd6 38. Kd4 Na2 39. Ke4 Nb4 40. Kf5
Nd5 41. Ba6 h4 42. Kg4 h3 43. Be2 h2 44. Bf3 Kc5 45. f5 Nf6+ 46. Kf4 Kb4 47. Ke5
Ng4+ 48. Kd5 Kxb3 0-1

[Event "Vienna"]
[Site "Vienna AUH"]
[Date "1882.05.17"]
[EventDate "1882.05.10"]
[Round "7"]
[Result "1-0"]
[White "Wilhelm Steinitz"]
[Black "Bernhard Fleissig"]
[ECO "C00"]
[WhiteElo "?"]
[BlackElo "?"]
[PlyCount "77"]

1. e4 e6 2. e5 d5 3. exd6 Bxd6 4. d4 Ne7 5. Bd3 Ng6 6. Nf3 Nc6
7. Nc3 Nb4 8. Bc4 c6 9. Ne4 Bc7 10. O-O O-O 11. Re1 Nd5
12. Nc5 Nh4 13. Ne5 Nf5 14. c3 Bxe5 15. Rxe5 Nf6 16. Re1 h6
17. Qf3 Nd5 18. Bb3 b6 19. Nd3 Ba6 20. Ne5 Rc8 21. Bc2 Nfe7
22. Qg3 Kh8 23. Qh4 Kg8 24. Qg3 Kh8 25. Qh3 Ng8 26. Qh5 Rc7
27. Bd2 Ndf6 28. Qh3 Nd5 29. c4 Ndf6 30. Rad1 Qe8 31. Bf4 Rc8
32. Qa3 Bb7 33. Qxa7 Ba8 34. Qxb6 g5 35. Bg3 Nd7 36. Qb3 f5
37. f3 Kg7 38. c5 Ndf6 39. Nc4 1-0
    """
    with DMFile(":memory:") as src:
        src.write(data)
        if obj.read_pgn(src) is False:
            return None
    return obj


def works_as_expected(data_name=None,
                      obj=None):
    """
        works_as_expected()

        works_as_expected() function for basic types defined DATA/UNAVAILABLE_DATA.


        _______________________________________________________________________

        (pimydoc)works_as_expected arguments and returned value
        ⋅All works_as_expected() functions are supposed to (1) say if <data_name> is in
        ⋅the scope of this function (2) and say if <obj> works as expected.
        ⋅
        ⋅ARGUMENTS:
        ⋅    o  data_name:   (None or str)data_name of the <obj>ect
        ⋅    o  obj:         (None or any object) object to be checked
        ⋅
        ⋅RETURNED VALUE:
        ⋅    (<obj> is None, <data_name> is not None) (bool)<data_name> is known
        ⋅    (<obj> is not None, <data_name> may be None or a str.) <obj> works as expected.
    """
    if len(obj) != 2:
        return False
    return obj[1].board.human_repr() == \
        "♝_♜_♛♜♞_\n" \
        "______♚_\n" \
        "__♟_♟♞_♟\n" \
        "__♙__♟♟_\n" \
        "__♘♙____\n" \
        "_♕___♙♗_\n" \
        "♙♙♗___♙♙\n" \
        "___♖♖_♔_"
