class Token:
    def __init__(self):
        self.y = 0
        self.x = 0
        self.board = []
        self.check = []

    def read(self):
        _, y, x = input().split()
        self.y = int(y)
        self.x = int(x[:-1])
        self.board = [[0] * self.x for _ in range(self.y)]
        self.check = [[False] * self.x for _ in range(self.y)]
        for cnt_y in range(self.y):
            map_line = input()
            for cnt_x in range(self.x):
                if map_line[cnt_x] == '.':
                    continue
                elif map_line[cnt_x] == '*':
                    self.board[cnt_y][cnt_x] = 1
                    self.check[cnt_y][cnt_x] = True

                else:
                    raise ValueError(f'Value Error| map.py| y:{cnt_y} x:{cnt_x}')
