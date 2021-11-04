class Mapping():
    """ THIS CODE IS OUR ORIGINAL!!!!!!!!!!
    DO YOU UNDERSTAND THIS MEAN?????
    YOU ARE REALLY LEARN PYTHON?????????
    WRITE CODE YOURSELF!!!!!!!!!!!!!!!!!!!!!!
    DO NOT COPYYYYYYYYY!!!!
    *********************
    **No Fill No Future**
    *********************
    """

    def __init__(self):
        self.y = 0
        self.x = 0
        self.board = []

    def read(self):
        _, y, x = input().split()
        self.y = int(y)
        self.x = int(x[:-1])  # To remove ':'
        _ = input()  # To remove "0123456789012345..."
        self.board = [[0] * self.x for _ in range(self.y)]
        for cnt_y in range(self.y):
            _, map_line = input().split()
            for cnt_x in range(self.x):
                if map_line[cnt_x] == '.':
                    continue
                elif map_line[cnt_x] == 'O' or map_line[cnt_x] == 'o':
                    self.board[cnt_y][cnt_x] = 1
                elif map_line[cnt_x] == 'X' or map_line[cnt_x] == 'x':
                    self.board[cnt_y][cnt_x] = 2
                else:
                    raise ValueError(f"Value Error| map.py| y:{cnt_y} x:{cnt_x}")
