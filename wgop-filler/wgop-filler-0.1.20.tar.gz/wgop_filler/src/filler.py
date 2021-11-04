
from typing import Dict, List, Tuple

class Token:
    def __init__(self, y=None, x=None):
        self.y = y
        self.x = x
        self.shape: List[str] = []

    def read(self) -> None:
        """標準入力からToken情報を読み取る"""
        self.y, self.x = map(int, input()[:-1].split(" ")[1:])
        self.shape = [input() for _ in range(self.y)]

class Board:
    def __init__(self, y: int = -1, x: int = -1) -> None:
        self.y = y
        self.x = x
        self.board: List[str] = []
        self.width = 0
        self.height = 0
        self.center_y = 0
        self.center_x = 0

    def read(self) -> None:
        """標準入力からBoard情報を読み取る"""
        self.y, self.x = map(int, input()[:-1].split(" ")[1:])
        _ = input()
        self.board = [input().split(" ")[1] for _ in range(self.y)]

        self.height = len(self.board)
        self.width = len(self.board[0])
        self.center_y = int(self.height / 2)
        self.center_x = int(self.width / 2)

class Player:
    def __init__(self, p_player_num: str) -> None:
        """Playerを初期化する

        Args:
            p_player_num (str): pPLAYER＿NUMBER (p1 or p2)
        """
        self.p = p_player_num
        self.char = "o" if self.p == "p1" else "x"
        self.enemy_char = "x" if self.char == "o" else "o"
        self.board = Board()
        self.token = Token()
        self.upper = 0
        self.right = 0
        self.lower = 0
        self.left = 0

    def is_enemy_char(self, cell: str) -> bool:
        """敵のマスか判定する"""
        return cell in (self.enemy_char, self.enemy_char.upper())

    def is_player_char(self, cell: str) -> bool:
        """自分のマスか判定する"""
        return cell in (self.char, self.char.upper())

    def put_random(self) -> bool:
        """playerが出力すべき情報を出力する

        Returns:
            bool: Tokenを当てはめられる座標が見つかったらTrue, そうでないならFalse
        """
        self.enemies = self.get_enemy_pos_list()
        self.check_my_cell()
        self.scores: Dict[Tuple[int, int], int] = {}
        if self.put_token():
            return True

        print("0 0")
        return False

    def put_token(self) -> bool:
        """Tokenを配置する座標を標準出力に出力する

        Returns:
            bool: tokenを当てはめられたか
        """
        board = self.board
        answers: List[Tuple[int, Tuple[int, int]]] = []

        for y in range(board.y):
            for x in range(board.x):
                # Tokenを当てはめられるなら、スコア（相手トークンとの距離値）と座標をリストに追加する
                if not self.check_overflow(x, y) and not self.check_overlap(x, y):
                    answers.append((self.calc_token_score(x, y), (y, x)))
        if answers:
            # 一番相手との距離が近い順に並べる
            answers.sort()
            answer = answers[0][1]
            print(f"{answer[0]} {answer[1]}")
            return True
        return False

    def calc_token_score(self, x: int, y: int) -> int:
        """Tokenを配置した場合のスコアを計算する"""
        score = 0
        for token_y in range(self.token.y):
            for token_x in range(self.token.x):
                if self.token.shape[token_y][token_x] != "*":
                    continue
                if self.board.board[token_y + y][token_x + x] != ".":
                    continue

                # 相手との距離測定
                score = self.calc_cell_score(token_x + x, token_y + y)

                # 相手との距離値指定以下になったら優先順位を下げる
                if score <= 1:
                    score = 1000
                    continue

                # 相手と接敵せず、真ん中が取られていない間は真ん中へ向かう
                elif self.board.board[self.board.center_y][self.board.center_x] == ".":
                    score = abs((token_y + y) - self.board.center_y) + abs((token_x + x) - self.board.center_x)

                # p1の場合
                elif self.p == "p1":
                    # 下壁到達後、右から下に向かう
                    if self.lower == 1 and self.right == 0:
                        if (token_y + y) >= (self.board.height - 6):
                            score = 2000
                            return score
                        for enemy in self.enemies:
                            if enemy[0] == (token_y + y):
                                score = 900
                                break
                        else:
                            score = abs((token_y + y) - (self.board.height - 1)) + abs((token_x + x) - (self.board.width - 1))

                    # p2なら右壁到達後、左から回り込んで右下に向かう
                    elif self.lower == 0 and self.right == 1:
                        for enemy in self.enemies:
                            if enemy[1] > (token_x + x):
                                score = 900
                                break
                            else:
                                score = abs((token_y + y) - (self.board.height - 1)) + abs((token_x + x) - (self.board.width - 1))

                    # 相手と接敵後、右下に一番近いところに置く
                    elif self.lower == 0 and self.right == 0:
                        score = abs((token_y + y) - (self.board.height - 1)) + abs((token_x + x) - (self.board.width - 1))

                # p2の場合
                elif self.p == "p2":
                    # p2なら上壁到達後、左から上に向かう
                    if self.upper == 1 and self.left == 0:
                        if (token_y + y) <= 0:
                            score = 2000
                            return score
                        for enemy in self.enemies:
                            if enemy[0] == (token_y + y):
                                score = 900
                                break
                        else:
                            score = abs((token_y + y) - 0) + abs((token_x + x) - 0)

                    # p2なら左壁到達後、右上に向かう
                    elif self.upper == 0 and self.left == 1:
                        score = abs((token_y + y) - 0) + abs((token_x + x) - (self.board.width - 1))

                    # p2なら相手と接敵後、左上に一番近いところに置く
                    elif self.upper == 0 and self.left == 0:
                        score = abs((token_y + y) - 0) + abs((token_x + x) - 0)
                else:
                    pass

        return score

    def calc_cell_score(self, x: int, y: int) -> int:
        """マスのスコアを返す

        敵の全トークンの中から
        (自分のy座標 - 相手のy座標) + (自分のx座標 - 相手のx座標)で
        一番小さい（座標が近い）数値を返す
        """
        score = self.scores.get((y, x))

        if score is None:
            score = min(
                [abs(y - enemy[0]) + abs(x - enemy[1]) for enemy in self.enemies]
            )
            self.scores[(y, x)] = score

        return score

    def get_enemy_pos_list(self) -> List[Tuple[int, int]]:
        """敵のマスリストを返す"""
        enemies: List[Tuple[int, int]] = []
        for y in range(self.board.y):
            for x in range(self.board.x):
                if self.is_enemy_char(self.board.board[y][x]):
                    enemies.append((y, x))
        return enemies

    def check_my_cell(self):
        """壁まで到達したか判定"""
        for x in range(self.board.width - 1):
            if self.is_player_char(self.board.board[0][x]):
                self.upper = 1
        for x in range(self.board.width - 1):
            if self.is_player_char(self.board.board[(self.board.height - 1)][x]):
                self.lower = 1
        for y in range(self.board.y):
            if self.is_player_char(self.board.board[y][0]):
                self.left = 1
            if self.is_player_char(self.board.board[y][(self.board.width - 1)]):
                self.right = 1

    def check_overflow(self, x: int, y: int) -> bool:
        """tokenがboardからはみ出ていないかチェックする

        Args:
            x (int): tokenを配置するx座標
            y (int): tokenを配置するy座標

        Returns:
            bool: はみ出ているならTrue
        """
        token = self.token
        board = self.board

        if ((x + token.x) > board.x) or ((y + token.y) > board.y):
            return True
        if (x < 0) or (y < 0):
            return True
        return False

    def check_overlap(self, x: int, y: int) -> bool:
        """tokenが敵のマスと重なっていないか、自分のマスと1つだけ重なっていないかを確認する

        Args:
            x (int): tokenを配置するx座標
            y (int): tokenを配置するy座標

        Returns:
            bool: 配置可能=False/配置不可=True
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
                    overlap_counter += 1

        if overlap_counter != 1:
            return True

        return False

def main() -> None:
    """fillerのmain部分"""
    _, _, p_player_num, _, _ = input().split(" ")

    player = Player(p_player_num)
    while True:
        player.board.read()
        player.token.read()
        player.put_random()
