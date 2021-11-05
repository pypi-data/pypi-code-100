from functools import reduce
import operator
from random import choice
from copy import deepcopy
from abc import ABC, abstractmethod


class Board(ABC):
    @abstractmethod
    def copy(self):
        pass

    @abstractmethod
    def get_next_player(self):
        pass

    @abstractmethod
    def move(self, col: int, row: int):
        pass

    @abstractmethod
    def get_free_hexes(self):
        pass

    @abstractmethod
    def get_winner(self):
        pass

    @abstractmethod
    def random_playout(self):
        pass

    @abstractmethod
    def random_playouts_won(self, num_playouts: int):
        pass

    @abstractmethod
    def get_dict(self):
        pass


class Yboard(Board):
    def __init__(self, size):
        self.board = [[0] * x for x in range(size, 0, -1)]

    def __str__(self):
        def row_size(row, max_size):
            if row < (max_size / 2):
                return row + 1
            else:
                return max_size - (row - 1)

        def columns_per_row(size):
            return [row_size(x, size - 1) for x in range(size)]

        def get_values(cpr, starting_col):
            return_list = []
            for row, columns in enumerate(cpr):
                xs = [(2 * x) + starting_col for x in range(columns)]
                ys = [y for y in range(row, -1, -1)]
                # return_list += [self.board[col][row] for col, row in zip(xs, ys)]
                return_list += [[i for i in zip(xs, ys)]]
            return return_list

        def value_to_rep(v):
            if v == 0:
                return '.'
            if v == 1:
                return 'X'
            if v == -1:
                return 'O'

        evens = get_values(columns_per_row(len(self.board)), 0)
        odds = get_values(columns_per_row(len(self.board) - 1), 1)
        zipped = reduce(operator.iconcat, list(zip(evens, odds)), [])
        if len(zipped) < len(evens) + len(odds):
            zipped += [evens[-1]]
        lines = ['     '.join([value_to_rep(self.board[x][y]) for x, y in i]) for i in zipped]
        for x in range(1, len(lines), 2):
            lines[x] = '   ' + lines[x]
        return '\n' + '\n'.join(lines) + '\n'

    def copy(self):
        b = Yboard(len(self.board))
        b.board = deepcopy(self.board)
        return b

    def get_next_player(self):
        board_sum = sum(reduce(operator.iconcat, self.board, []))
        if board_sum == 1:
            return -1
        elif board_sum == 0:
            return 1
        else:
            return 0  # Not a valid Y board

    def move(self, col, row):
        player = self.get_next_player()
        if player == 0:
            raise Exception('Attempted to move on an invalid board.')
        if self.board[col][row] != 0:
            raise Exception('Attempted to move on a non-empty hex.')
        self.board[col][row] = player
        return self

    def get_free_hexes(self):
        return [(col,row) for col in range(len(self.board)) for row in range(len(self.board[col])) if self.board[col][row] == 0]

    def _assign(self, col, row, player):
        self.board[col][row] = player

    def get_winner(self):
        if len(self.board) == 1:
            return self.board[0][0]
        if len(self.board) == 2:
            already_seen = set()
            for col, col_values in enumerate(self.board):
                for row, value in enumerate(col_values):
                    if value in already_seen:
                        return value
                    else:
                        already_seen.add(value)
            return 0
        else:
            reduced_board = Yboard(len(self.board) - 1)
            for col, col_values in enumerate(self.board[:-1]):
                for row, value in enumerate(col_values[:-1]):
                    sub_board = Yboard(2)
                    sub_board._assign(0, 0, self.board[col][row])
                    sub_board._assign(0, 1, self.board[col][row+1])
                    sub_board._assign(1, 0, self.board[col+1][row])
                    reduced_board._assign(col, row, sub_board.get_winner())
            return reduced_board.get_winner()

    def random_playout(self):
        moves = self.get_free_hexes()
        while self.get_winner() == 0:
            self.move(*choice(moves))
            moves = self.get_free_hexes()
        return self

    def random_playouts_won(self, num_playouts):
        wins = {1: 0, -1: 0}
        for _ in range(num_playouts):
            b = self.copy()
            b.random_playout()
            wins[b.get_winner()] += 1
        return wins

    def get_dict(self):
        return {"cell{},{}".format(x, y): self.board[x][y] for x in range(len(self.board)) for y in range(len(self.board[x]))}


class Hexboard(Board):
    def __init__(self, size):
        self.size = size
        self.yboard = Yboard(size * 2)
        for col in range(size):
            height = size - col
            for row in range(height):
                self.yboard._assign(col, row, 1)
                self.yboard._assign(col, (2 * size - col) - row - 1, -1)

    def __str__(self):
        return self.yboard.__str__()

    def _hex_to_y(self, col, row):
        return (
            col + row + 1,
            self.size - col - 1
        )

    def _y_to_hex(self, col, row):
        return (
            row - self.size + 1,
            col - row + self.size - 2
        )

    def copy(self):
        b = Hexboard(self.size)
        b.yboard.board = deepcopy(self.yboard.board)
        return b

    def get_next_player(self):
        return self.yboard.get_next_player()

    def move(self, col: int, row: int):
        ycol, yrow = self._hex_to_y(col, row)
        self.yboard.move(ycol, yrow)
        return self

    def get_free_hexes(self):
        free_y_hexes = self.yboard.get_free_hexes()
        return map(self._y_to_hex, free_y_hexes)

    def get_winner(self):
        return self.yboard.get_winner()

    def random_playout(self):
        self.yboard.random_playout()
        return self

    def random_playouts_won(self, num_playouts):
        return self.yboard.random_playouts_won(num_playouts)

    def get_dict(self):
        hexes = [self._hex_to_y(x,y) for x in range(self.size) for y in range(self.size)]
        hex_dict = {hex:self.yboard.board[hex[0]][hex[1]] for hex in hexes}
        return {"cell{},{}".format(hex[0], hex[1]):hex_dict[hex] for hex in hex_dict}
