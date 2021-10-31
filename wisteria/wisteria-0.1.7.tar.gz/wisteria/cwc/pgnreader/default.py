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
    Wisteria project : wisteria/wisteria/cwc/pgnreader/default.py

    Default cwc/PGN reader+writer using only the following types:
    - bool, int, str
    - dict, list, tuple
        Note that dicts may have non string keys.
    ___________________________________________________________________________

    PGN reader+writer (https://en.wikipedia.org/wiki/Portable_Game_Notation).
    Regular chess only; no sophisticated rules (but castling, en passant and
    promotion are known). This is a very simple version of what a real PGN reader/writer might
    look like: no optimized storage, no move validation.

    With this module you can read a .pgn file, play the game move by move and write the game in
    another file. PGN-files containing several games are correctly read and written.

    No move validation: a move is always assumed to be valid.
    Data other than the moves (events, player names, dates and so on) are
    stored but are not used.

    A PGN viewer allowing to show giant games (cf tests/game5.pgn) may be find at:
            https://fr.chesstempo.com/pgn-viewer/


    ___________________________________________________________________________

    o  COLOR_NOCOLOR, COLOR_WHITE, COLOR_BLACK
    o  invert_color(color)
    o  PIECENATURE_NOPIECE, PIECENATURE_PAWN, PIECENATURE_ROOK, PIECENATURE_KNIGHT
       PIECENATURE_BISHOP, PIECENATURE_QUEEN, PIECENATURE_KING
    o  PIECENATURE2ALGEBRICNOTATION / ALGEBRICNOTATION2PIECENATURE
    o  MOVETYPE_SINGLE, MOVETYPE_CAPTURE, MOVETYPE_CASTLING

    o  ChessError class
    o  ChessGameTags class
    o  ChessPiece class
    o  ChessMove class
    o  ChessListOfMoves class
    o  ChessGameStatus class
    o  ChessBoard class
    o  ChessGame class
    o  ChessGames class

    o  fill(obj)
    o  works_as_expected()
"""
# For this demonstration file, some writing rules are not respected:
#   pylint: disable=invalid-name
#   pylint: disable=too-few-public-methods
#   pylint: disable=too-many-nested-blocks
#   pylint: disable=too-many-arguments
import copy
import re
from dataclasses import dataclass

COLOR_NOCOLOR = 0
COLOR_WHITE = 1
COLOR_BLACK = 2


def invert_color(color):
    """invert_color((int)color)"""
    if color == COLOR_WHITE:
        return COLOR_BLACK
    return COLOR_WHITE


PIECENATURE_NOPIECE = 0
PIECENATURE_PAWN = 1
PIECENATURE_ROOK = 2
PIECENATURE_KNIGHT = 3
PIECENATURE_BISHOP = 4
PIECENATURE_QUEEN = 5
PIECENATURE_KING = 6
PIECENATURE2ALGEBRICNOTATION = {
    PIECENATURE_ROOK: 'R',
    PIECENATURE_KNIGHT: 'N',
    PIECENATURE_BISHOP: 'B',
    PIECENATURE_QUEEN: 'Q',
    PIECENATURE_KING: 'K'}
ALGEBRICNOTATION2PIECENATURE = {value: key for key, value in PIECENATURE2ALGEBRICNOTATION.items()}

MOVETYPE_SINGLE = 0
MOVETYPE_CAPTURE = 1
MOVETYPE_CASTLING_OO = 2
MOVETYPE_CASTLING_OOO = 3


class ChessError(Exception):
    """
        ChessError class

        Unique error raised by the program.
    """


class ChessGameTags(dict):
    """
        ChessGameTags class

        Use this class to store tags read in .pgn files like these ones:

            [Event "F/S Return Match"]
            [Site "Belgrade, Serbia JUG"]
            [Date "1992.11.04"]
            [Round "29"]
            [White "Fischer, Robert J."]
            [Black "Spassky, Boris V."]
            [Result "1/2-1/2"]


        _______________________________________________________________________

        o  __eq__(self, other)
        o  __init__(self, datadict=None)
        o  __repr__(self)
    """
    def __eq__(self,
               other):
        """
            ChessGamesTags.__eq__()

            Stricly speaking, not required to read/write PGN files but required
            to check that everything "works as expected" (see cwc validation).

            ___________________________________________________________________

            ARGUMENT: (ChessGamesTags)other, the object compared to self

            RETURNED VALUE: (bool)True if other == self
        """
        return dict.__eq__(self, other)

    def __init__(self,
                 datadict=None):
        """ChessGameTags.__init__()"""
        dict.__init__(self)
        if datadict:
            for key, value in datadict:
                self[key] = value

    def __repr__(self):
        """ChessGameTags.__repr__()"""
        return "; ".join(f"{key}: {value}" for key, value in self.items())


@dataclass
class ChessPiece:
    """
        ChessPiece class

        _______________________________________________________________________

        o  piece2unicode/unicode2piece

        o  (int)color, e.g. COLOR_WHITE
        o  (int)nature, e.g. PIECENATURE_PAWN

        o  __eq__(self, other)
    """
    color: int = COLOR_NOCOLOR
    nature: int = PIECENATURE_NOPIECE

    piece2unicode = {
        (PIECENATURE_NOPIECE, COLOR_NOCOLOR): '_',
        (PIECENATURE_PAWN, COLOR_WHITE): '♙',
        (PIECENATURE_PAWN, COLOR_BLACK): '♟',
        (PIECENATURE_ROOK, COLOR_WHITE): '♖',
        (PIECENATURE_ROOK, COLOR_BLACK): '♜',
        (PIECENATURE_KNIGHT, COLOR_WHITE): '♘',
        (PIECENATURE_KNIGHT, COLOR_BLACK): '♞',
        (PIECENATURE_BISHOP, COLOR_WHITE): '♗',
        (PIECENATURE_BISHOP, COLOR_BLACK): '♝',
        (PIECENATURE_QUEEN, COLOR_WHITE): '♕',
        (PIECENATURE_QUEEN, COLOR_BLACK): '♛',
        (PIECENATURE_KING, COLOR_WHITE): '♔',
        (PIECENATURE_KING, COLOR_BLACK): '♚',
        }
    unicode2piece = {value: key for key, value in piece2unicode.items()}

    def __eq__(self,
               other):
        """ChessPiece.__eq__()"""
        return self.color == other.color and self.nature == other.nature

    def __repr__(self):
        """ChessPiece.__repr__()"""
        return f"ChessPiece: {self.color=}; {self.nature=}"

    def human_repr(self):
        """ChessPiece.human_repr()"""
        return ChessPiece.piece2unicode[self.nature, self.color]

    def init_from_unicode_string(self,
                                 string):
        """ChessPiece.init_from_unicode_string()"""
        self.nature, self.color = ChessPiece.unicode2piece[string]
        return self

    def is_empty(self):
        """ChessPiece.is_empty()"""
        return self.color == COLOR_NOCOLOR and self.nature == PIECENATURE_NOPIECE


@dataclass
class ChessMove:
    """
        ChessMove class


        _______________________________________________________________________

        o  (int)movetype, e.g. MOVETYPE_SINGLE
        o  (iterable)beforeafter_coord_piece1, e.g. ((0,0), (1,1))
        o  (iterable)beforeafter_coord_piece2, e.g. ((0,0), (1,1))
        o  (None|int)promotion, e.g. PIECENATURE_QUEEN
        o  (bool)enpassant
        o  (str)str_game_result, e.g. "0-1"

        o  __eq__(self, other)
        o  __repr__(self)
    """
    beforeafter_coord_piece1: tuple
    beforeafter_coord_piece2: tuple
    movetype: int = MOVETYPE_SINGLE
    promotion: int = None
    enpassant: bool = False
    str_game_result: str = None

    def __eq__(self,
               other):
        """
            ChessMove.__eq__()

            Stricly speaking, not required to read/write PGN files but required
            to check that everything "works as expected" (see cwc validation).

            ___________________________________________________________________

            ARGUMENT: (ChessMove)other, the object compared to self

            RETURNED VALUE: (bool)True if other == self
        """
        return self.movetype == other.movetype and \
            self.beforeafter_coord_piece1 == other.beforeafter_coord_piece1 and \
            self.beforeafter_coord_piece2 == other.beforeafter_coord_piece2 and \
            self.promotion == other.promotion and \
            self.enpassant == other.enpassant and \
            self.str_game_result == other.str_game_result

    def __repr__(self):
        """ChessMove.__repr__()"""
        return f"{self.movetype=}; " \
            f"{self.beforeafter_coord_piece1=}; {self.beforeafter_coord_piece2}; " \
            f"{self.promotion=}; {self.enpassant=}; {self.str_game_result=};"


@dataclass
class ChessListOfMoves(list):
    """
        ChessListOfMoves class

        A list of ((int)doublemove_number, (int)self.next_player, (ChessMove)move)


        _______________________________________________________________________

        o  (int)next_player
        o  (int)doublemove_number

        o  __eq__(self, other)
        o  __repr__(self)
        o  add_move(self, move)
        o  who_plays(self)
    """
    next_player: int = COLOR_WHITE
    doublemove_number: int = 1

    def __eq__(self,
               other):
        """
            ChessListOfMoves.__eq__()

            Stricly speaking, not required to read/write PGN files but required
            to check that everything "works as expected" (see cwc validation).

            ___________________________________________________________________

            ARGUMENT: (ChessListOfMoves)other, the object compared to self

            RETURNED VALUE: (bool)True if other == self
        """
        return list.__eq__(self, other) and \
            self.next_player == other.next_player and \
            self.doublemove_number == other.doublemove_number

    def __repr__(self):
        """ChessListOfMoves.__repr__()"""
        return f"list of moves: {self.next_player=}; {self.doublemove_number=}; " + \
            "; ".join(repr(move) for move in self)

    def add_move(self,
                 move):
        """
            ChessListOfMoves.add_move()

            This move is played by self.next_player
        """
        self.append((self.doublemove_number, self.next_player, move))

        if self.next_player == COLOR_WHITE:
            self.next_player = COLOR_BLACK
        else:
            self.next_player = COLOR_WHITE
            self.doublemove_number += 1

    def who_plays(self):
        """ChessListOfMoves.who_plays()"""
        return self.next_player


@dataclass
class ChessGameStatus:
    """
        ChessGameStatus class


        _______________________________________________________________________

        o  (bool)game_is_over
        o  (int)who_won, e.g. COLOR_BLACK

        o  __eq__(self, other)
        o  __repr__(self)
        o  copy(self)
        o  update_from_pgn_string(self,
                               status_string,
                               current_player)
    """
    game_is_over: bool = False
    who_won: int = COLOR_NOCOLOR

    def __eq__(self,
               other):
        """
            ChessGameStatus.__eq__()

            Stricly speaking, not required to read/write PGN files but required
            to check that everything "works as expected" (see cwc validation).

            ___________________________________________________________________

            ARGUMENT: (ChessGameStatus)other, the object compared to self

            RETURNED VALUE: (bool)True if other == self
        """
        return self.game_is_over == other.game_is_over and \
            self.who_won == other.who_won

    def __repr__(self):
        """ChessGameStatus.__repr__()"""
        return f"{self.game_is_over=}; {self.who_won=}"

    def copy(self):
        """ChessGameStatus.copy()"""
        return ChessGameStatus(game_is_over=self.game_is_over,
                               who_won=self.who_won)

    def update_from_pgn_string(self,
                               status_string,
                               current_player):
        """
            ChessGameStatus.update_from_pgn_string()

            Beware ! if you modify this method, please update
                    ChessGame.regex_pgn_listofmoves['game_result']
        """
        if status_string == "1/2-1/2":
            self.game_is_over = True
            self.who_won = COLOR_NOCOLOR
        elif status_string == "0-1":
            self.game_is_over = True
            self.who_won = COLOR_BLACK
        elif status_string == "1-0":
            self.game_is_over = True
            self.who_won = COLOR_WHITE
        elif status_string == "*":
            self.game_is_over = False
            self.who_won = None
        elif status_string == "++":
            self.game_is_over = True
            self.who_won = current_player
        else:
            raise ChessError(f"Unknown status string '{status_string}'.")


class ChessBoard:
    """
        ChessBoard class


        _______________________________________________________________________

        o  moves_descr

        o  (dict)board
        o  (ChessGameStatus)pieces_status

        o  __eq__(self, other)
        o  __init__(self)
        o  __repr__(self)
        o  copy(self)
        o  get_king_coord(self, color)
        o  get_xy(self)
        o  human_repr(self)
        o  init_from_unicode_string(self, string)
        o  is_empty_or_is_this_piece(self, xy, piece)
        o  is_kingpinned(self, xy0, xy1)
        o  iter_through_all_squares()
        o  set_startpos(self)
        o  set_xy(self, xy, value)
        o  set_xy_empty(self, xy)
        o  update_by_playing_a_move(self, move)
        o  which_piece_could_go_to(self, piece, coord_after, movetype)
        o  who_attacks(self, xy)
        o  xy_is_off_the_board(xy)
    """
    # moves description for all pieces but knight and pawn
    # moves[nature] = (deltamax, ((deltax, deltay), ...))
    moves_descr = {PIECENATURE_BISHOP: (8,
                                        ((+1, -1), (+1, +1), (-1, +1), (-1, -1)),),
                   PIECENATURE_ROOK: (8,
                                      ((0, -1), (0, +1), (-1, 0), (+1, 0)),),
                   PIECENATURE_QUEEN: (8,
                                       ((+1, -1), (+1, +1), (-1, +1), (-1, -1),
                                        (0, -1), (0, +1), (-1, 0), (+1, 0)),),
                   PIECENATURE_KING: (2,
                                      ((+1, -1), (+1, +1), (-1, +1), (-1, -1),
                                       (0, -1), (0, +1), (-1, 0), (+1, 0)),),
                   }

    def __eq__(self,
               other):
        """
            ChessBoard.__eq__()

            Stricly speaking, not required to read/write PGN files but required
            to check that everything "works as expected" (see cwc validation).

            ___________________________________________________________________

            ARGUMENT: (ChessBoard)other, the object compared to self

            RETURNED VALUE: (bool)True if other == self
        """
        return self.board == other.board and \
            self.pieces_status == other.pieces_status

    def __init__(self):
        """ChessBoard.__init__()"""
        self.board = {}  # cf .get_xy(), set_xy()
        self.pieces_status = ChessGameStatus()

        self.set_startpos()

    def __repr__(self):
        """ChessBoard.__repr__()"""
        return self.human_repr() + repr(self.pieces_status)

    def copy(self):
        """ChessBoard.copy()"""
        res = ChessBoard()
        res.board = copy.deepcopy(self.board)
        res.pieces_status = self.pieces_status.copy()
        return res

    def get_king_coord(self,
                       color):
        """
            ChessBoard.copy()

            Return the (x, y) of the <color>(white/black) king
        """
        for xy in self.iter_through_all_squares():
            obj = self.get_xy(xy)
            if obj.nature == PIECENATURE_KING and \
               obj.color == color:
                return xy
        raise ChessError(f"No king (color: {color}): {self.human_repr()}")

    def get_xy(self,
               xy):
        """ChessBoard.get_xy()"""
        return self.board[xy[0], xy[1]]

    def human_repr(self):
        """ChessBoard.human_repr()"""
        res = []
        for y in range(8):
            res.append("".join(self.get_xy((x, y)).human_repr() for x in range(8)))
        return "\n".join(res)

    def init_from_unicode_string(self,
                                 string):
        """ChessBoard.init_from_unicode_string()"""
        index = 0
        for xy in self.iter_through_all_squares():
            self.set_xy(xy, ChessPiece().init_from_unicode_string(string[index]))
            index += 1

    def is_empty_or_is_this_piece(self,
                                  xy,
                                  piece):
        """
            ChessBoard.get_xy()

            Return True if [x, y] is an empty square OR if [x, y] is <piece>
        """
        obj = self.get_xy(xy)
        return obj.is_empty() or obj == piece

    def is_kingpinned(self,
                      xy0,
                      xy1):
        """
            ChessBoard.is_kingpinned()

            Return True if board[x0, y0] moving to bord[x1, y1] is impossible since board[x0, y0]
            is a king pinned piece.
        """
        # <piece> is the piece that may be pinned:
        piece = self.get_xy(xy0)
        # <king> is the king of <piece>:
        king = self.get_king_coord(piece.color)
        len0 = len(self.who_attacks(king))

        # <board> is an alternative board with <piece> being moved to (x1, y1):
        _board = self.copy()
        _board.set_xy_empty(xy0)
        _board.set_xy(xy1, piece)
        # the king may have just moved, so we update his position:
        king = _board.get_king_coord(piece.color)
        len1 = len(_board.who_attacks(king))

        return len0 < len1

    @staticmethod
    def iter_through_all_squares():
        """ChessBoard.iter_through_all_squares()"""
        for y in range(8):
            for x in range(8):
                yield x, y

    def set_startpos(self):
        """ChessBoard.set_startpos()"""
        self.board = {}
        self.pieces_status = ChessGameStatus()

        for xy in self.iter_through_all_squares():
            self.set_xy(xy, ChessPiece())

        self.init_from_unicode_string("♜♞♝♛♚♝♞♜"
                                      "♟♟♟♟♟♟♟♟"
                                      "________"
                                      "________"
                                      "________"
                                      "________"
                                      "♙♙♙♙♙♙♙♙"
                                      "♖♘♗♕♔♗♘♖")

    def set_xy(self,
               xy,
               value):
        """ChessBoard.set_xy()"""
        self.board[xy[0], xy[1]] = value

    def set_xy_empty(self,
                     xy):
        """ChessBoard.set_xy_empty()"""
        self.set_xy(xy, ChessPiece())

    def update_by_playing_a_move(self,
                                 move):
        """
            ChessBoard.update_by_playing_a_move()

            Modify <self> by playing a <move>.
        """
        if move.movetype in (MOVETYPE_SINGLE, MOVETYPE_CAPTURE):
            before, after = move.beforeafter_coord_piece1
            piece = self.get_xy(before)
            self.set_xy_empty(before)
            if not move.promotion:
                self.set_xy(after, piece)
            else:
                self.set_xy(after, ChessPiece(nature=move.promotion,
                                              color=piece.color))

            if move.enpassant:
                if piece.color == COLOR_WHITE:
                    self.set_xy_empty((after[0], after[1]+1))
                else:
                    self.set_xy_empty((after[0], after[1]-1))

        elif move.movetype in (MOVETYPE_CASTLING_OO, MOVETYPE_CASTLING_OOO):
            # king:
            before, after = move.beforeafter_coord_piece1
            piece = self.get_xy(before)
            self.set_xy_empty(before)
            self.set_xy(after, piece)
            # rook:
            before, after = move.beforeafter_coord_piece2
            piece = self.get_xy(before)
            self.set_xy_empty(before)
            self.set_xy(after, piece)

    def which_piece_could_go_to(self,
                                piece,
                                coord_after,
                                movetype):
        """
            ChessBoard.which_piece_could_go_to()

            Where does the <piece> that will arrive on <coord_after> come from?

            More than one result may be returned !
        """
        def add_to_res_if_rightpiece_notpinned(_xy, coord_after, piece):
            if not ChessBoard.xy_is_off_the_board(_xy) and \
               self.get_xy(_xy) == piece and \
               not self.is_kingpinned(_xy, coord_after):
                res.append(_xy)

        x, y = coord_after
        res = []

        if piece.nature == PIECENATURE_PAWN:
            if movetype == MOVETYPE_SINGLE:
                if piece.color == COLOR_WHITE:
                    if y == 4 and self.get_xy((x, y+1)).is_empty():
                        add_to_res_if_rightpiece_notpinned((x, y+2), coord_after, piece)
                    else:
                        add_to_res_if_rightpiece_notpinned((x, y+1), coord_after, piece)
                else:  # piece.color == COLOR_BLACK
                    if y == 3 and self.get_xy((x, y-1)).is_empty():
                        add_to_res_if_rightpiece_notpinned((x, y-2), coord_after, piece)
                    else:
                        add_to_res_if_rightpiece_notpinned((x, y-1), coord_after, piece)
            elif movetype == MOVETYPE_CAPTURE:
                if piece.color == COLOR_WHITE:
                    add_to_res_if_rightpiece_notpinned((x+1, y+1), coord_after, piece)
                    add_to_res_if_rightpiece_notpinned((x-1, y+1), coord_after, piece)
                else:
                    add_to_res_if_rightpiece_notpinned((x+1, y-1), coord_after, piece)
                    add_to_res_if_rightpiece_notpinned((x-1, y-1), coord_after, piece)

        elif piece.nature == PIECENATURE_KNIGHT:
            add_to_res_if_rightpiece_notpinned((x-2, y-1), coord_after, piece)
            add_to_res_if_rightpiece_notpinned((x-2, y+1), coord_after, piece)
            add_to_res_if_rightpiece_notpinned((x+2, y-1), coord_after, piece)
            add_to_res_if_rightpiece_notpinned((x+2, y+1), coord_after, piece)
            add_to_res_if_rightpiece_notpinned((x-1, y-2), coord_after, piece)
            add_to_res_if_rightpiece_notpinned((x-1, y+2), coord_after, piece)
            add_to_res_if_rightpiece_notpinned((x+1, y-2), coord_after, piece)
            add_to_res_if_rightpiece_notpinned((x+1, y+2), coord_after, piece)
        elif piece.nature in (PIECENATURE_BISHOP,
                              PIECENATURE_ROOK,
                              PIECENATURE_QUEEN,
                              PIECENATURE_KING):
            deltamax = ChessBoard.moves_descr[piece.nature][0]
            for deltax, deltay in ChessBoard.moves_descr[piece.nature][1]:
                for delta in range(1, deltamax):
                    # ~~
                    if ChessBoard.xy_is_off_the_board((x+(deltax*delta), y+(deltay*delta))):
                        # we have to try another (deltax, deltay)
                        break
                    if self.is_empty_or_is_this_piece((x+(deltax*delta), y+(deltay*delta)), piece):
                        add_to_res_if_rightpiece_notpinned((x+(deltax*delta),
                                                            y+(deltay*delta)),
                                                           coord_after,
                                                           piece)
                        if self.get_xy((x+(deltax*delta), y+(deltay*delta))) == piece:
                            break
                    else:
                        break

        return res

    def who_attacks(self,
                    xy):
        """ChessBoard.who_attacks()"""

        def add_to_res_if_rightpiece(xy, piece):
            if not ChessBoard.xy_is_off_the_board(xy) and \
               self.get_xy(xy) == piece:
                res.append(xy)

        target = self.get_xy(xy)
        _color = invert_color(target.color)
        res = []

        x, y = xy

        # ---- do a pawn attack (x, y) ? --------------------------------------
        piece = ChessPiece(color=_color,
                           nature=PIECENATURE_PAWN)
        if target.color == COLOR_WHITE:
            add_to_res_if_rightpiece((x+1, y-1), piece)
            add_to_res_if_rightpiece((x-1, y-1), piece)
        else:
            add_to_res_if_rightpiece((x+1, y+1), piece)
            add_to_res_if_rightpiece((x-1, y+1), piece)

        # ---- do a knight attack (x, y) ? ------------------------------------
        piece = ChessPiece(color=_color,
                           nature=PIECENATURE_KNIGHT)
        add_to_res_if_rightpiece((x-2, y-1), piece)
        add_to_res_if_rightpiece((x-2, y+1), piece)
        add_to_res_if_rightpiece((x+2, y-1), piece)
        add_to_res_if_rightpiece((x+2, y+1), piece)
        add_to_res_if_rightpiece((x-1, y-2), piece)
        add_to_res_if_rightpiece((x-1, y+2), piece)
        add_to_res_if_rightpiece((x+1, y-2), piece)
        add_to_res_if_rightpiece((x+1, y+2), piece)

        # ---- do a bishop/rook/queen/king attack (x, y) ? --------------------
        for nature in (PIECENATURE_BISHOP,
                       PIECENATURE_ROOK,
                       PIECENATURE_QUEEN,
                       PIECENATURE_KING):
            piece = ChessPiece(color=_color,
                               nature=nature)
            deltamax = ChessBoard.moves_descr[nature][0]
            for deltax, deltay in ChessBoard.moves_descr[nature][1]:
                for delta in range(1, deltamax):
                    # ~~
                    if ChessBoard.xy_is_off_the_board((x+(deltax*delta), y+(deltay*delta))):
                        # we have to try another (deltax, deltay):
                        break
                    if self.is_empty_or_is_this_piece((x+(deltax*delta), y+(deltay*delta)), piece):
                        add_to_res_if_rightpiece((x+(deltax*delta),
                                                  y+(deltay*delta)),
                                                 piece)
                        if self.get_xy((x+(deltax*delta), y+(deltay*delta))) == piece:
                            break
                    else:
                        break

        return res

    @staticmethod
    def xy_is_off_the_board(xy):
        """ChessBoard.xy_is_off_the_board()"""
        return not ((0 <= xy[0] <= 7) and (0 <= xy[1] <= 7))


class ChessGame:
    """
        ChessGame class


        _______________________________________________________________________

        o  regex_pgn_tags
        o  regex_pgn_listofmoves
        o  regex_simplemove_algebraicnotation
        o  regex_simplemove_algebraicnotation2
        o  strcoord2coord / coord2strcoord

        o  (ChessGameTags)chessgame_tags
        o  (ChessBoard)board
        o  (ChessListOfMoves)listofmoves
        o  (ChessGameStatus)status
        o  (list of str)errors

        o  __eq__(self, other)
        o  __init__(self)
        o  __repr__(self)
        o  read_pgn(self, lines)
        o  read_pgn__doublemove(self, str_doublemove)
        o  read_pgn__listofmoves(self, src)
        o  read_pgn__simplemove(self, str_simplemove)
        o  write_pgn(self)
        o  write_pgn__listofmoves(self)
        o  write_pgn__simplemove(self, move)
    """
    # e.g. [Event "F/S Return Match"]
    regex_pgn_tags = re.compile(r'^\s*\[(?P<key>.+)\s+\"(?P<value>.+)\"\]$')

    regex_pgn_listofmoves = {
        'doublemovenumber': re.compile(r'[\d]+\.\s'),
        # Beware ! if you modify 'game_result', please update
        # ChessGameStatus.update_from_pgn_string().
        'game_result': re.compile(r'(?P<pre>.+)(?P<game_result>1\/2-1\/2|1\-0|0\-1|#|\*|\+\+)'),
        'en passant': re.compile(r'\s*e\.p\.'),
    }
    regex_simplemove_algebraicnotation = re.compile(
        r"^"
        r"(?P<str_piecenature>[KQNRB])?"
        r"(?P<str_intersymb>[x|\-])?"
        r"(?P<str_coord_x1>[a-h]|[1-8]|[a-h][1-8])"
        r"(=(?P<str_promotion>[KQNRB]))?"
        r"(?P<str_chess>\+)?"
        r"(?P<str_enpassant>e\.p\.)?"
        r"$")
    regex_simplemove_algebraicnotation2 = re.compile(
        r"^"
        r"(?P<str_piecenature>[KQNRB])?"
        r"(?P<str_coord_x0>[a-h][1-8]|[a-h]|[1-8])?"
        r"(?P<str_intersymb>[x|\-])?"
        r"(?P<str_coord_x1>[a-h][1-8]|[a-h]|[1-8])"
        r"(=(?P<str_promotion>[KQNRB]))?"
        r"(?P<str_chess>\+)?"
        r"(?P<str_enpassant>e\.p\.)?"
        r"$")

    strcoord2coord = {
        'a8': (0, 0), 'b8': (1, 0), 'c8': (2, 0), 'd8': (3, 0),
        'e8': (4, 0), 'f8': (5, 0), 'g8': (6, 0), 'h8': (7, 0),
        'a7': (0, 1), 'b7': (1, 1), 'c7': (2, 1), 'd7': (3, 1),
        'e7': (4, 1), 'f7': (5, 1), 'g7': (6, 1), 'h7': (7, 1),
        'a6': (0, 2), 'b6': (1, 2), 'c6': (2, 2), 'd6': (3, 2),
        'e6': (4, 2), 'f6': (5, 2), 'g6': (6, 2), 'h6': (7, 2),
        'a5': (0, 3), 'b5': (1, 3), 'c5': (2, 3), 'd5': (3, 3),
        'e5': (4, 3), 'f5': (5, 3), 'g5': (6, 3), 'h5': (7, 3),
        'a4': (0, 4), 'b4': (1, 4), 'c4': (2, 4), 'd4': (3, 4),
        'e4': (4, 4), 'f4': (5, 4), 'g4': (6, 4), 'h4': (7, 4),
        'a3': (0, 5), 'b3': (1, 5), 'c3': (2, 5), 'd3': (3, 5),
        'e3': (4, 5), 'f3': (5, 5), 'g3': (6, 5), 'h3': (7, 5),
        'a2': (0, 6), 'b2': (1, 6), 'c2': (2, 6), 'd2': (3, 6),
        'e2': (4, 6), 'f2': (5, 6), 'g2': (6, 6), 'h2': (7, 6),
        'a1': (0, 7), 'b1': (1, 7), 'c1': (2, 7), 'd1': (3, 7),
        'e1': (4, 7), 'f1': (5, 7), 'g1': (6, 7), 'h1': (7, 7),

        'a': (0, None), 'b': (1, None), 'c': (2, None), 'd': (3, None),
        'e': (4, None), 'f': (5, None), 'g': (6, None), 'h': (7, None),

        '1': (None, 7), '2': (None, 6), '3': (None, 5), '4': (None, 4),
        '5': (None, 3), '6': (None, 2), '7': (None, 1), '8': (None, 0),
        }
    coord2strcoord = {value: key for key, value in strcoord2coord.items()}

    def __eq__(self,
               other):
        """
            ChessGame.__eq__()

            Stricly speaking, not required to read/write PGN files but required
            to check that everything "works as expected" (see cwc validation).

            ___________________________________________________________________

            ARGUMENT: (ChessGame)other, the object compared to self

            RETURNED VALUE: (bool)True if other == self
        """
        return self.chessgame_tags == other.chessgame_tags and \
            self.board == other.board and \
            self.listofmoves == other.listofmoves and \
            self.status == other.status and \
            self.errors == other.errors

    def __init__(self):
        """ChessGame.__init__()"""
        self.chessgame_tags = ChessGameTags()
        self.board = ChessBoard()
        self.listofmoves = ChessListOfMoves()
        self.status = ChessGameStatus()

        self.errors = []

    def __repr__(self):
        """ChessGame.__repr__()"""
        res = f"{self.chessgame_tags=}; " \
            f"{self.board=}; {self.listofmoves=}; {self.status=}"
        if self.errors:
            res += "errors: "+str(self.errors)
        return res

    def read_pgn(self,
                 lines):
        """ChessGame.read_pgn()"""
        success = True

        self.listofmoves = ChessListOfMoves()
        try:
            str_listofmoves = []
            for _line in lines:
                line = _line.strip()

                if line:
                    regex_pgn__found = False
                    if res_regex_pgn_tags := re.search(ChessGame.regex_pgn_tags, line):
                        regex_pgn__found = True
                        self.chessgame_tags[res_regex_pgn_tags.group('key')] = \
                            res_regex_pgn_tags.group('value')

                    if regex_pgn__found is False:
                        str_listofmoves.append(line)

            str_listofmoves = " ".join(str_listofmoves)

            self.read_pgn__listofmoves(str_listofmoves)

        except ChessError as error:
            self.errors.append(error)
            success = False

        return success

    def read_pgn__doublemove(self,
                             str_doublemove):
        """ChessGame.read_pgn__doublemove()"""
        # " e.p." with space(s) must be rewritten "e.p." (without space)
        if re.search(ChessGame.regex_pgn_listofmoves['en passant'], str_doublemove):
            str_doublemove = re.sub(ChessGame.regex_pgn_listofmoves['en passant'],
                                    "e.p.",
                                    str_doublemove)
        # if <str_doublemove> is something like:
        #   "Kd5 Kxb3 0-1"
        # we have to attach the last part using the '_' character:
        #   "Kd5 Kxb3_0-1"
        if res__game_result := re.search(ChessGame.regex_pgn_listofmoves['game_result'],
                                         str_doublemove):
            self.status.update_from_pgn_string(status_string=res__game_result.group('game_result'),
                                               current_player=self.listofmoves.next_player)
            str_doublemove = re.sub(
                ChessGame.regex_pgn_listofmoves['game_result'],
                lambda match: match.group('pre').strip()+'_'+match.group('game_result').strip(),
                str_doublemove)

        if " " not in str_doublemove:
            # only one move in <str_doublemove> (as in 'Nc4')
            self.read_pgn__simplemove(str_doublemove)
        else:
            # normal case, two moves in <str_doublemove> (as in 'e4 e5')
            move1, move2 = str_doublemove.split(" ")
            self.read_pgn__simplemove(move1)
            self.read_pgn__simplemove(move2)

    def read_pgn__listofmoves(self,
                              src):
        """
            ChessGame.read_pgn__listofmoves()

            src: (list of str)listofmoves
        """
        doublemove_number = 0
        for _str_doublemove in re.split(ChessGame.regex_pgn_listofmoves['doublemovenumber'], src):
            str_doublemove = _str_doublemove.strip()
            if str_doublemove:
                doublemove_number += 1
                self.read_pgn__doublemove(str_doublemove)

    def read_pgn__simplemove(self,
                             str_simplemove):
        """simplemove: e6e4 // e6-e4 // e4"""

        # ---------------------------------------------------------------------
        # ---- let's remove from <str_simplemove> the game result. ------------
        # ---------------------------------------------------------------------
        str_game_result = None
        if res__game_result := re.search(ChessGame.regex_pgn_listofmoves['game_result'],
                                         str_simplemove):
            str_game_result = res__game_result.group('game_result')

            # let's remove the '_' character added by read_pgn__doublemove() before the game result:
            str_simplemove = str_simplemove.replace('_', '')
            # we can now remove the game result suffix (e.g. '1-0')
            self.status.update_from_pgn_string(status_string=res__game_result.group('game_result'),
                                               current_player=self.listofmoves.next_player)
            str_simplemove = re.sub(
                ChessGame.regex_pgn_listofmoves['game_result'],
                lambda match: match.group('pre').strip(),
                str_simplemove)

        str_simplemove = str_simplemove.strip()

        # ---------------------------------------------------------------------
        # ---- let's extract from str_simplemove the move details -------------
        # ---------------------------------------------------------------------

        # default values:
        who_plays = self.listofmoves.who_plays()
        movetype = MOVETYPE_SINGLE  # default value, may be changed.
        # if movetype is MOVETYPE_SINGLE, <piece1_coord_before> will be automatically
        # computed with the help of .which_piece_could_go_to():
        piece1_coord_before = None
        piece1_coord_after = None
        piece2_coord_before = None
        piece2_coord_after = None
        promotion = None  # if promotion, <promotion> will be the PIECENATURE_xxx constant
        enpassant = False

        # ---- let's try to initialize <piece1_coord_before> and --------------
        # ---- <piece1_coord_after> from <str_simplemove>. --------------------
        if str_simplemove == "O-O":
            movetype = MOVETYPE_CASTLING_OO
            # king
            piece1_coord_before = self.board.get_king_coord(color=who_plays)
            piece1_coord_after = piece1_coord_before[0]+2, piece1_coord_before[1]
            # rook:
            piece2_coord_before = piece1_coord_before[0]+3, piece1_coord_before[1]
            piece2_coord_after = piece1_coord_before[0]+1, piece1_coord_before[1]
        elif str_simplemove == "O-O-O":
            movetype = MOVETYPE_CASTLING_OOO
            # king
            piece1_coord_before = self.board.get_king_coord(color=who_plays)
            piece1_coord_after = piece1_coord_before[0]-2, piece1_coord_before[1]
            # rook:
            piece2_coord_before = piece1_coord_before[0]-4, piece1_coord_before[1]
            piece2_coord_after = piece1_coord_before[0]-1, piece1_coord_before[1]
        else:
            res_algebricnotation = {"str_piecenature": None,
                                    "str_coord_x0": None,
                                    "str_intersymb": None,
                                    "str_coord_x1": None,
                                    "str_promotion": None,
                                    "str_chess": None,
                                    "str_enpassant": None,
                                    }

            if _res := re.search(ChessGame.regex_simplemove_algebraicnotation,
                                 str_simplemove):
                res_algebricnotation["str_piecenature"] = _res.group("str_piecenature")
                res_algebricnotation["str_intersymb"] = _res.group("str_intersymb")
                res_algebricnotation["str_coord_x1"] = _res.group("str_coord_x1")
                res_algebricnotation["str_promotion"] = _res.group("str_promotion")
                res_algebricnotation["str_chess"] = _res.group("str_chess")
                res_algebricnotation["str_enpassant"] = _res.group("str_enpassant")
            elif _res := re.search(ChessGame.regex_simplemove_algebraicnotation2,
                                   str_simplemove):
                res_algebricnotation["str_piecenature"] = _res.group("str_piecenature")
                res_algebricnotation["str_coord_x0"] = _res.group("str_coord_x0")
                res_algebricnotation["str_intersymb"] = _res.group("str_intersymb")
                res_algebricnotation["str_coord_x1"] = _res.group("str_coord_x1")
                res_algebricnotation["str_promotion"] = _res.group("str_promotion")
                res_algebricnotation["str_chess"] = _res.group("str_chess")
                res_algebricnotation["str_enpassant"] = _res.group("str_enpassant")
            else:
                raise ChessError(
                    f"Ill-formed or unknown string format for str_simplemove='{str_simplemove}'.")

            if res_algebricnotation["str_intersymb"] == "x":
                movetype = MOVETYPE_CAPTURE

            if res_algebricnotation["str_piecenature"] is not None:
                # str_piecenature: 'Q' / 'K' / 'R' / 'B' / 'N'
                piece1_piecenature = \
                    ALGEBRICNOTATION2PIECENATURE[res_algebricnotation["str_piecenature"]]
            else:
                # no piecenature: it's a pawn
                piece1_piecenature = PIECENATURE_PAWN

            if res_algebricnotation["str_coord_x0"] is None:  # coord_x0 wasn't given (e.g. 'Rxb4')
                piece1_coord_after = ChessGame.strcoord2coord[res_algebricnotation["str_coord_x1"]]
            else:  # coord_x0 was given, at least partially (e.g. 'cxb5', 'Rbxb4')
                # piece1_coord_before > maybe partial (e.g. 'Rbb4')
                piece1_coord_before = ChessGame.strcoord2coord[res_algebricnotation["str_coord_x0"]]
                piece1_coord_after = ChessGame.strcoord2coord[res_algebricnotation["str_coord_x1"]]

                if piece1_coord_before[1] is None:
                    # <piece1_coord_before> is only partially initialized: we only have the column,
                    # as in 'Qab2', 'cxb5'
                    for _x, _y in self.board.which_piece_could_go_to(
                            piece=ChessPiece(nature=piece1_piecenature,
                                             color=self.listofmoves.next_player),
                            coord_after=piece1_coord_after,
                            movetype=movetype):
                        if _x == piece1_coord_before[0]:
                            # a tuple would not be writable:
                            piece1_coord_before = list(piece1_coord_before)
                            piece1_coord_before[1] = _y  # we found the row
                            piece1_coord_before = tuple(piece1_coord_before)
                            #
                            # To optimize, you may want to consider the first solution is the right
                            # one and therefore add 'break'; without this 'break' statement you may
                            # find errors in the list of moves.
                            #
                            # break

                elif piece1_coord_before[0] is None:
                    # <piece1_coord_before> is only partially initialized: we only have the row,
                    # as in 'Q2b2'.
                    for _x, _y in self.board.which_piece_could_go_to(
                            piece=ChessPiece(nature=piece1_piecenature,
                                             color=self.listofmoves.next_player),
                            coord_after=piece1_coord_after,
                            movetype=movetype):
                        if _y == piece1_coord_before[1]:
                            # a tuple would not be writable:
                            piece1_coord_before = list(piece1_coord_before)
                            piece1_coord_before[0] = _x  # we found the column
                            piece1_coord_before = tuple(piece1_coord_before)
                            #
                            # To optimize, you may want to consider the first solution is the right
                            # one and therefore add 'break'; without this 'break' statement you may
                            # find errors in the list of moves.
                            #
                            # break

            if res_algebricnotation["str_promotion"]:
                promotion = ALGEBRICNOTATION2PIECENATURE[res_algebricnotation["str_promotion"]]

            if piece1_coord_after[0] is None or piece1_coord_after[1] is None:
                raise ChessError(f"Can't understand this (simple) move: {str_simplemove} .")

        # ---- special case: piece1_coord_before has not yet been initialized -
        # It happens if <str_simplemove> contains an extra character to remove
        # any ambiguity.
        if piece1_coord_before is None:
            _possi = self.board.which_piece_could_go_to(
                piece=ChessPiece(nature=piece1_piecenature,
                                 color=self.listofmoves.next_player),
                coord_after=piece1_coord_after,
                movetype=movetype)
            if not _possi:
                raise ChessError(
                    f"Can't interpret (simple) move '{str_simplemove}' for the current board. "
                    f"No legal move matches this string. "
                    f"self={repr(self)}")
            if len(_possi) > 1:
                raise ChessError(
                    f"Anomaly: too many possibilities, the move '{str_simplemove}' is ambiguous. "
                    f"Current situation is: {repr(self)}")
            # [0] since there is only ONE POSSIBILITY here: len(_possi) is 1.
            piece1_coord_before = _possi[0]

        # ---- en passant ? ---------------------------------------------------
        enpassant = movetype == MOVETYPE_CAPTURE and \
            self.board.get_xy((piece1_coord_after[0], piece1_coord_after[1])).is_empty()

        # ---- new_move, update of .listofmoves and .board ----------------
        new_move = ChessMove(movetype=movetype,
                             beforeafter_coord_piece1=(piece1_coord_before, piece1_coord_after),
                             beforeafter_coord_piece2=(piece2_coord_before, piece2_coord_after),
                             promotion=promotion,
                             enpassant=enpassant,
                             str_game_result=str_game_result)
        self.listofmoves.add_move(new_move)
        self.board.update_by_playing_a_move(new_move)

    def write_pgn(self):
        """ChessGame.write_pgn()"""
        res = []

        for key, value in self.chessgame_tags.items():
            res.append(f'[{key} "{value}"]')

        res.append("")

        res.extend(self.write_pgn__listofmoves())

        return res

    def write_pgn__listofmoves(self):
        """ChessGame.write_pgn__listofmoves()"""
        res = []

        self.board.set_startpos()

        doublemove_str = ""
        for simplemove_index, (doublemove_index, _, simplemove) in enumerate(self.listofmoves):
            if simplemove_index % 2 == 0:
                # white plays:
                doublemove_str = str(doublemove_index)+". " + self.write_pgn__simplemove(simplemove)
            else:
                # black plays:
                doublemove_str += " " + self.write_pgn__simplemove(simplemove)
                res.append(doublemove_str)
                doublemove_str = ""

        if doublemove_str:
            res.append(doublemove_str)

        return res

    def write_pgn__simplemove(self,
                              move):
        """ChessGame.write_pgn__simplemove()"""
        piece1 = self.board.get_xy(move.beforeafter_coord_piece1[0])

        _possi = None
        if move.movetype in (MOVETYPE_SINGLE, MOVETYPE_CAPTURE):
            _possi = self.board.which_piece_could_go_to(piece1,
                                                        move.beforeafter_coord_piece1[1],
                                                        move.movetype)

        self.board.update_by_playing_a_move(move)

        if move.movetype == MOVETYPE_CASTLING_OO:
            return "O-O"

        if move.movetype == MOVETYPE_CASTLING_OOO:
            return "O-O-O"

        res = ""
        if piece1.nature != PIECENATURE_PAWN:
            res += PIECENATURE2ALGEBRICNOTATION[piece1.nature]

        if len(_possi) == 1:
            if piece1.nature == PIECENATURE_PAWN and move.movetype == MOVETYPE_CAPTURE:
                # 'd' in 'dxe5'
                res += ChessGame.coord2strcoord[(move.beforeafter_coord_piece1[0][0], None)]
            else:
                pass
        else:
            if piece1.nature == PIECENATURE_PAWN:
                # 'd' in 'dxe5'
                res += ChessGame.coord2strcoord[(move.beforeafter_coord_piece1[0][0], None)]
            else:
                # The ambiguity must be resolved by specifying only the column ('a', 'b', ...) or,
                # if the column does not resolve the ambiguity, only the row ('1', '2', ...);
                # otherwise, the column and row must be written.
                #
                # E.g. if beforeafter_coord_piece1[0] is equal to (2, 0) (==[c8]),
                # we count the number of times (int)2 appears in _possi: it must
                # appear at last one time(*); if it's the case, there's no ambiguity to add only
                # the column; it (int)2 appears more than one time, the ambiguity is not resolved.
                #
                # (*) Why at least one time ? Because among _possiilites lies the right move, the
                #     one that has been chosen. If this possibility is ambiguous, other moves will
                #     add their column/row.
                if tuple(_x for _x, _y in _possi).count(move.beforeafter_coord_piece1[0][0]) == 1:
                    res += ChessGame.coord2strcoord[(move.beforeafter_coord_piece1[0][0], None)]
                elif tuple(_y for _x, _y in _possi).count(move.beforeafter_coord_piece1[0][1]) == 1:
                    res += ChessGame.coord2strcoord[(None, move.beforeafter_coord_piece1[0][1])]
                else:
                    res += ChessGame.coord2strcoord[move.beforeafter_coord_piece1[0]]

        if move.movetype == MOVETYPE_SINGLE:
            res += ChessGame.coord2strcoord[move.beforeafter_coord_piece1[1]]
        elif move.movetype == MOVETYPE_CAPTURE:
            res += "x"+ChessGame.coord2strcoord[move.beforeafter_coord_piece1[1]]

        if move.promotion:
            res += "="+PIECENATURE2ALGEBRICNOTATION[move.promotion]

        if move.enpassant:
            res += " e.p."

        if move.str_game_result:
            res += " " + move.str_game_result

        return res


class ChessGames(list):
    """
        ChessGames class


        _______________________________________________________________________

        o  __eq__(self, other)
        o  read_pgn(self, pgnfilename)
        o  write_pgn(self, pgnfilename)
    """
    def __eq__(self,
               other):
        """
            ChessGames.__eq__()

            Stricly speaking, not required to read/write PGN files but required
            to check that everything "works as expected" (see cwc validation).

            ___________________________________________________________________

            ARGUMENT: (ChessGames)other, the object compared to self

            RETURNED VALUE: (bool)True if other == self
        """
        return list.__eq__(self, other)

    def read_pgn(self,
                 src):
        """ChessGames.read_pgn()"""
        success = True

        inside_header = False
        buff = []

        for _line in src:
            line = _line.strip()

            if line:
                if inside_header:
                    if re.search(ChessGame.regex_pgn_tags, line) and not line.startswith("1. "):
                        # we're still in the header.
                        pass
                    else:
                        # we're not in the header anymore.
                        inside_header = False
                else:
                    if re.search(ChessGame.regex_pgn_tags, line) and not line.startswith("1. "):
                        # we weren't in the header but <line> is a header line.
                        if buff:
                            game = ChessGame()
                            success = success and game.read_pgn(buff)
                            self.append(game)
                        buff = []
                        inside_header = True
                    else:
                        # we're still reading data lines that are not in a header.
                        if line.startswith("1. "):
                            if buff:
                                game = ChessGame()
                                success = success and game.read_pgn(buff)
                                self.append(game)
                            buff = []

                buff.append(line)

        if buff:
            game = ChessGame()
            success = success and game.read_pgn(buff)
            self.append(game)

        return success

    def write_pgn(self,
                  dest):
        """ChessGames.write_pgn()"""
        for game in self:
            for line in game.write_pgn():
                dest.write(line+"\n")
            dest.write("\n")
