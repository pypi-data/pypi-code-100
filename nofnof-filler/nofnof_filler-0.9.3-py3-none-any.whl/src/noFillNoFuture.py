from copy import deepcopy, copy
from mapping import Mapping
from token import Token

""" THIS CODE IS OUR ORIGINAL!!!!!!!!!! """
""" DO YOU UNDERSTAND THIS MEAN?????"""
""" YOU ARE REALLY LEARN PYTHON????????? """
""" WRITE CODE YOURSELF!!!!!!!!!!!!!!!!!!!!!!!"""
"""DO NOT COPYYYYYYYYY"""


# NofNof_filler
class NoFillNoFuture:
    def __init__(self):
        _, _, p_num, _, _ = input().split(" ")
        if p_num == "p1":
            self.p_num = 1
        elif p_num == "p2":
            self.p_num = 2
        else:
            raise ValueError(f"Value Error| NoFillNoFuture| p_num:{p_num}")
        self.mapping = Mapping(self.p_num)
        self.token = Token(self.p_num)
        # self.first_token_x = 0
        # self.first_token_y = 0
        # self.first_mapping_x = 0
        # self.first_mapping_y = 0
        self.coordinate_mapping_y = 0
        self.coordinate_mapping_x = 0

    def search_for_token(self):
        #  only overlapped point ##
        for token_y in range(self.token.y):
            for token_x in range(self.token.x):
                if self.token.board[token_y][token_x] == 1:
                    is_ok = self.search_for_mapping(copy(token_y), copy(token_x))

    def search_for_mapping(self, token_y, token_x) -> bool:
        is_answer = False
        for mapping_y in range(self.mapping.y):
            for mapping_x in range(self.mapping.x):
                if self.mapping.board[mapping_y][mapping_x] == self.p_num \
                        and self.check_token_recur(deepcopy(self.token.check), token_y, token_x, \
                                                   mapping_y, mapping_x, 0):
                    is_answer = True
                    #  print(f"token: {token_y}, {token_x}\n")
                    self.coordinate_mapping_y = mapping_y - token_y
                    self.coordinate_mapping_x = mapping_x - token_x
        return is_answer

    def check_token_recur(self, temp_token: list, token_y: int, token_x: int, mapping_y: int, mapping_x: int,
                          depth: int) -> bool:
        # first in this function: self.mapping.check,
        temp_token[token_y][token_x] = False

        if sum([l_token.count(True) for l_token in temp_token]) == 0:
            self.coordinate_mapping_y = mapping_y - token_y
            self.coordinate_mapping_x = mapping_x - token_x
            return True

        # right
        if self.is_token_valid('r', token_y, token_x):
            if self.is_mapping_valid('r', mapping_y, mapping_x):
                if not self.check_token_recur(temp_token, token_y, token_x + 1, mapping_y, mapping_x + 1, depth + 1):
                    return False
            else:
                return False  # quit recursive function

        # down
        if self.is_token_valid('d', token_y, token_x):
            if self.is_mapping_valid('d', mapping_y, mapping_x):
                if not self.check_token_recur(temp_token, token_y + 1, token_x, mapping_y + 1, mapping_x, depth + 1):
                    return False
            else:
                return False
        # left
        if self.is_token_valid('l', token_y, token_x):
            if self.is_mapping_valid('l', mapping_y, mapping_x):
                if not self.check_token_recur(temp_token, token_y, token_x - 1, mapping_y, mapping_x - 1, depth + 1):
                    return False
            else:
                return False
        # up
        if self.is_token_valid('u', token_y, token_x):
            if self.is_mapping_valid('u', mapping_y, mapping_x):
                if not self.check_token_recur(temp_token, token_y - 1, token_x, mapping_y - 1, mapping_x, depth + 1):
                    return False
            else:
                return False

    def is_mapping_valid(self, direction: str, mapping_y: int, mapping_x) -> bool:
        if direction == 'r' and mapping_x + 1 < self.mapping.x \
                and self.mapping.board[mapping_y][mapping_x + 1] == 0:
            return True
        elif direction == 'd' and mapping_y + 1 < self.mapping.y \
                and self.mapping.board[mapping_y + 1][mapping_x] == 0:
            return True
        elif direction == 'l' and mapping_x > 0 \
                and self.mapping.board[mapping_y][mapping_x - 1] == 0:
            return True
        elif direction == 'u' and mapping_y > 0 \
                and self.mapping.board[mapping_y - 1][mapping_x] == 0:
            return True
        return False

    def is_token_valid(self, direction: str, token_y: int, token_x: int) -> bool:
        if direction == 'r' and token_x + 1 < self.token.x \
                and self.token.board[token_y][token_x + 1] == 1:
            return True
        elif direction == 'd' and token_y + 1 < self.token.y \
                and self.token.board[token_y + 1][token_x] == 1:
            return True
        elif direction == 'l' and token_x > 0 \
                and self.token.board[token_y][token_x - 1] == 1:
            return True
        elif direction == 'u' and token_y > 0 \
                and self.token.board[token_y - 1][token_x] == 1:
            return True
        return False

    # don't use!! ##
    # def search_for_mapping_recur(self, temp_mapping, mapping_y, mapping_x):
    #     # first : self.mapping.check
    #     temp_mapping[mapping_y][mapping_x] = False
    #     self.search_for_token_recur(self.token.check, self.first_token_y \
    #                                 , self.first_token_x, mapping_y, mapping_x)
    #     # right
    #     if mapping_x < self.mapping.x and temp_mapping[mapping_y][mapping_x + 1]:
    #         self.search_for_token_recur(temp_mapping, mapping_y, mapping_x + 1)
    #     # down
    #     if mapping_y < self.mapping.y and temp_mapping[mapping_y + 1][mapping_x]:
    #         self.search_for_token_recur(temp_mapping, mapping_y + 1, mapping_x)
    #     # left
    #     if mapping_x > 0 and temp_mapping[mapping_y][mapping_x - 1]:
    #         self.search_for_token_recur(temp_mapping, mapping_y, mapping_x - 1)
    #     # up
    #     if mapping_y > 0 and temp_mapping[mapping_y - 1][mapping_x]:
    #         self.search_for_token_recur(temp_mapping, mapping_y - 1, mapping_x)

    def init_before_search(self):
        # self.first_token_x = 0
        # self.first_token_y = 0
        # self.first_mapping_x = 0
        # self.first_mapping_y = 0
        self.coordinate_mapping_y = 0
        self.coordinate_mapping_x = 0
        self.token.num = 0

    def search(self):
        self.mapping.read()
        self.token.read()
        self.init_before_search()
        self.search_for_token()


