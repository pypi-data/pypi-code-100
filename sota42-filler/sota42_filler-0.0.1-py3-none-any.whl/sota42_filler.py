#!/usr/local/bin/python3


class Token:
    def __init__(self):
        self.y: int = -1  # token height
        self.x: int = -1  # tokenj width
        self.shape: list[str] = []  # list of string consist of ( "." or "*" ).

    def read(self) -> None:
        """Read Token info fron stdout."""
        self.y, self.x = map(int, input()[:-1].split(" ")[1:])
        self.shape = [input() for _ in range(self.y)]


class Board:
    def __init__(self) -> None:
        self.y: int = -1  # board height
        self.x: int = -1  # board width
        self.board = (
            []
        )  # list of string consist of ( "." or "o" or "x" or "O" or "X" ).  : List[ str ]
        self.init_position: tuple = None  # Player's initial position on board:(x, y)
        self.corner_2nd: tuple = None  # not most far and not most near corner from self.init_position of bord: (x, y)
        self.corner_3rd: tuple = None  # not most far and not most near corner from self.init_position of bord: (x, y)

    def read(self, p_char: str) -> None:
        """Read Board info fron stdout."""
        self.y, self.x = map(int, input()[:-1].split(" ")[1:])
        _ = input()
        self.board = [input().split(" ")[1] for _ in range(self.y)]
        if self.init_position is None:
            # initialize init_position
            y = 0
            for row in self.board:
                x = row.find(p_char.upper())
                if x > -1:
                    self.init_position = (x, y)
                    break
                y += 1

            # initialize corner_2nd, corner_3rd
            if y < (self.y / 2):
                if x < (self.x / 2):
                    self.corner_2nd = (0, self.y - 1)
                    self.corner_3rd = (self.x - 1, 0)
                else:
                    self.corner_2nd = (0, 0)
                    self.corner_3rd = (self.x - 1, self.y - 1)
            else:
                if x < (self.x / 2):
                    self.corner_2nd = (0, 0)
                    self.corner_3rd = (self.x - 1, self.y - 1)
                else:
                    self.corner_2nd = (self.x - 1, 0)
                    self.corner_3rd = (0, self.y - 1)


class Player:
    def __init__(self, player_num: str) -> None:
        """
        Args:
            p_player_num : str : "p1" or "p2"
        """
        self.p = player_num  # "p1" or "p2"
        self.char = "o" if self.p == "p1" else "x"
        self.enemy_char = "x" if self.char == "o" else "o"
        self.board = Board()
        self.token = Token()
        self.second_edge = None
        self.third_edge = None
        self.first_position = None
        self.turn_num = 0.0

    def is_enemy_char(self, cell: str) -> bool:
        return cell.upper() == self.enemy_char.upper()

    def is_player_char(self, cell: str) -> bool:
        return cell.upper() == self.char.upper()

    def put_move(self) -> bool:
        """Print information that Player should output
        Returns:
            bool: if find the coordinates to which the token can be placed,return True.
            else, return False.
        """
        self.enemies = self.get_enemy_pos_list()
        self.scores = {}  # Dict[Tuple[int, int], int]

        return self.put_token()

    def put_token(self) -> bool:
        """Print the coordinates to place the Token to the standard output, and return placeable

        Returns:
            bool: can be placed?
        """
        board = self.board
        answers = []  # List[Tuple[int, Tuple[int, int]]]

        for y in range(board.y):
            for x in range(board.x):
                if not (self.is_overflow(x, y) or self.is_too_overlap(x, y)):
                    # Add score and candidate coordinates to the list.
                    answers.append((self.calc_token_score(x, y), (y, x)))
        if answers:
            answers.sort()
            answer = answers[0][1]
            print(f"{answer[0]} {answer[1]}")
            return True

        print("0 0")
        return False

    def calc_token_score(self, x: int, y: int) -> int:
        """Calculate the score when Token is placed."""
        score = 0
        for token_y in range(self.token.y):
            for token_x in range(self.token.x):
                if self.token.shape[token_y][token_x] != "*":  # yuukoububunn
                    continue
                if self.board.board[token_y + y][token_x + x] != ".":  #
                    continue
                score += self.calc_cell_score(token_x + x, token_y + y)
        
        self.turn_num += 0.001
        weight1 = 0.75 + 2 * self.turn_num
        weight2 = 0.15 - self.turn_num
        weight3 = 0.10 - self.turn_num
        x_c = x + (self.token.x//2)
        y_c = y + (self.token.y//2)

        return int(
            score * weight1
            + self.calc_evaluation_value_from_corner(x_c, y_c, self.board.corner_2nd)
            * weight2
            + self.calc_evaluation_value_from_corner(x_c, y_c, self.board.corner_3rd)
            * weight3
        )

    def calc_cell_score(self, x: int, y: int) -> int:
        """return evaluation value from cell of enemy"""
        score = self.scores.get((y, x))
        if score is None:
            score = min(
                [abs(y - enemy[0]) + abs(x - enemy[1]) for enemy in self.enemies]
            )
            self.scores[(y, x)] = score
        return score

    def calc_evaluation_value_from_corner(self, x: int, y: int, corner: tuple):
        """return evaluation value from center of token(x, y) to corner  """
        return abs(x - corner[0]) + abs(y - corner[1])

    def get_enemy_pos_list(self):  # -> List[Tuple[int, int]]
        """return list of enemy's cells"""
        enemies = []  # List[Tuple[int, int]]
        for y in range(self.board.y):
            for x in range(self.board.x):
                if self.is_enemy_char(self.board.board[y][x]):
                    enemies.append((y, x))
        return enemies

    def is_overflow(self, x: int, y: int) -> bool:
        """Check if the token is out of the board

        Args:
            x (int): x-coordinate to place token
            y (int): y-coordinate to place token
        Returns:
            bool: is overflow?
        """
        token = self.token
        board = self.board

        if ((x + token.x) > board.x) or ((y + token.y) > board.y):
            return True
        if (x < 0) or (y < 0):
            return True
        return False

    def is_too_overlap(self, x: int, y: int) -> bool:
        """Check that the token does not overlap the enemy's cell or only one of mine

        Args:
            x (int): x-coordinate to place token
            y (int): y-coordinate to place token

        Returns:
            bool: is too overlap?
        """
        token = self.token
        overlap_counter = 0

        for token_y in range(token.y):
            for token_x in range(token.x):
                if token.shape[token_y][token_x] != "*":
                    continue
                if self.is_enemy_char(self.board.board[y + token_y][x + token_x]):
                    return True
                if self.is_player_char(self.board.board[y + token_y][x + token_x]):
                    if overlap_counter == 0:
                        overlap_counter += 1
                    else:
                        return True

        return overlap_counter != 1


def main() -> None:
    """main process of filler"""
    _, _, player_num, _, _ = input().split(" ")

    player = Player(player_num)
    p_char = player.char
    try:
        while True:
            # infinite loop
            player.board.read(p_char)
            player.token.read()
            player.put_move()
    except EOFError:
        return


if __name__ == "__main__":
    main()
