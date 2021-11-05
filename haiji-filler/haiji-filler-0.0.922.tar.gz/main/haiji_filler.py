#!/usr/bin/env python3

from heapq import heapify, heappop, heappush

OUR_MARK, RIVAL_MARK = "", ""

BOARD_Y, BOARD_X = -1, -1
BOARD = []

TOKEN_Y, TOKEN_X = -1, -1
TOKEN = []
TOKEN_UL_Y, TOKEN_UL_X = -1, -1
TOKEN_LR_Y, TOKEN_LR_X = -1, -1

MAX_DIST = 0

def main():
    global OUR_MARK, RIVAL_MARK
    message = list(input().split(' '))
    our_id = int(message[2][1])
    if our_id == 1: OUR_MARK, RIVAL_MARK = 'o', 'x'
    else: OUR_MARK, RIVAL_MARK = 'x', 'o'
    game_start()

def game_start():
    while True:
        input_board()
        # output_board()
        input_token()
        # output_token()
        # distance_haiji_to_rival()
        # sum_of_evaluation()
        # sum_to_heapq()
        # numbers_of_around()
        last_check()
        # output_next_yx()

def board_or_game_end(_input):
    if _input[0] == "=":
        # print('game end')
        exit()
    else: return

def input_board():
    global BOARD, BOARD_Y, BOARD_X
    _input = input()
    board_or_game_end(_input)
    _input = list(_input.split(' '))
    BOARD_Y, BOARD_X = int(_input[1]), int(_input[2][:-1])
    _none = input()

    BOARD = []
    for _ in range(BOARD_Y):
        _input = input().split(' ')
        BOARD.append(list(_input[1]))
    return

def output_board():
    global BOARD, BOARD_Y, BOARD_X
    print('>', BOARD_Y, BOARD_X)
    for p in BOARD:
        print('>', ''.join(p))
    return

def input_token():
    global  TOKEN, TOKEN_Y, TOKEN_X
    _input = list(input().split(' '))
    TOKEN_Y, TOKEN_X = int(_input[1]), int(_input[2][:-1])
    TOKEN = []
    for _ in range(TOKEN_Y):
        TOKEN.append(list(input()))
    return

def output_token():
    global TOKEN, TOKEN_Y, TOKEN_X
    print('>', TOKEN_Y, TOKEN_X)
    for token in TOKEN:
        print('>', ''.join(token))
    return

def token_upperleft_lowerright():
    global TOKEN, TOKEN_UL_Y, TOKEN_UL_X, TOKEN_LR_Y, TOKEN_LR_X
    first = True
    for i, row in enumerate(TOKEN):
        if '*' in row:
            if first:
                TOKEN_UL_Y = i
                first = False
            else: TOKEN_LR_Y = i
    first = True
    for i, col in enumerate(zip(*TOKEN)):
        if '*' in col:
            if first:
                TOKEN_UL_X = i
                first = False
            else: TOKEN_LR_X = i
    return

def last_check():
    scores = sum_of_evaluation()
    output_next_yx_2(scores)

def sum_of_evaluation():
    global BOARD_Y, BOARD_X, MAX_DIST
    sum_points = [[0]*BOARD_X for _ in range(BOARD_Y)]

    distance_hq = distance_haiji_to_rival()
    len_dis = len(distance_hq)
    while distance_hq:
        dis, y, x = heappop(distance_hq)
        sum_points[y][x] += len_dis
        len_dis -= 1

    num_of_haiji_around, num_of_rival_around = numbers_of_around()
    points = [0, MAX_DIST/4, MAX_DIST/2, MAX_DIST*3/4, MAX_DIST]
    for i in range(BOARD_Y):
        for j in range(BOARD_X):
            sum_points[i][j] += points[num_of_haiji_around[i][j]]
            sum_points[i][j] += points[num_of_rival_around[i][j]]
    return sum_points

def numbers_of_around():
    global BOARD, BOARD_Y, BOARD_X, RIVAL_MARK
    num_of_haiji_around = [[0]*BOARD_X for _ in range(BOARD_Y)]
    num_of_rival_around = [[0]*BOARD_X for _ in range(BOARD_Y)]
    for i in range(BOARD_Y):
        for j in range(BOARD_X):
            if BOARD[i][j] == '.': continue
            count = 0
            for dy, dx in zip([0, 1, 0, -1], [1, 0, -1, 0]):
                ny, nx = i+dy, j+dx
                if not (0 <= ny < BOARD_Y and 0 <= nx < BOARD_X): continue
                if BOARD[ny][nx] == '.': count += 1
            if BOARD[i][j] in (RIVAL_MARK.lower(), RIVAL_MARK.upper()): num_of_rival_around[i][j] += count
            else: num_of_haiji_around[i][j] += count
    return num_of_haiji_around, num_of_rival_around

def get_all_place():
    global BOARD, BOARD_Y, BOARD_X, RIVAL_MARK
    haiji_place, rival_place = [], []
    for i in range(BOARD_Y):
        for j in range(BOARD_X):
            board = BOARD[i][j]
            if board == '.': continue
            if board in (RIVAL_MARK.lower(), RIVAL_MARK.upper()):
                rival_place.append((i, j))
                continue
            haiji_place.append((i, j))
    return haiji_place, rival_place

def distance_haiji_to_rival():
    global MAX_DIST
    dist_haiji_to_rival = []
    heapify(dist_haiji_to_rival)
    haiji_place, rival_place = get_all_place()
    for hi, hj in (haiji_place):
        min_dist = float('inf')
        for ri, rj in rival_place:
            dst = ((ri-hi)**2 + (rj-hj)**2)**0.5
            MAX_DIST = max(MAX_DIST, dst)
            min_dist =  min(min_dist, dst)
        heappush(dist_haiji_to_rival, (min_dist, hi, hj))
    return dist_haiji_to_rival

def output_next_yx_2(scores):
    global OUR_MARK, RIVAL_MARK, BOARD, BOARD_Y, BOARD_X, TOKEN_Y, TOKEN_X, TOKEN_LR_Y, TOKEN_LR_X
    max_score = []
    heapify(max_score)
    for i in range(BOARD_Y):
        for j in range(BOARD_X):
            if not (i + TOKEN_Y <= BOARD_Y and j + TOKEN_X <= BOARD_X):
                break
            count_haiji_mark = 0
            count_rival_mark = 0
            total_score = 0
            for ci in range(TOKEN_Y):
                for cj in range(TOKEN_X):
                    ny = i + ci
                    nx = j + cj
                    if BOARD[ny][nx] == '.': continue
                    if TOKEN[ci][cj] == '.': continue
                    if BOARD[ny][nx] in (RIVAL_MARK.lower(), RIVAL_MARK.upper()):
                        count_rival_mark += 1
                    else:
                        count_haiji_mark += 1
                        total_score += scores[ny][nx]
            if count_rival_mark == 0 and count_haiji_mark == 1:
                heappush(max_score, (-total_score, i, j))
    _score, i, j = heappop(max_score)
    print(i, j)
    return

if __name__ == '__main__':
    main()
