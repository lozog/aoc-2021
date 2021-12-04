from copy import deepcopy
from pprint import pprint

BINGO_DIM = 5

def process_bingo_input(file):
    """
    reads the input file and returns the list of bingo inputs
    and a list of boards, represented as 2D arrays
    """
    input_file = open(file, 'r')
    inputs = [int(i) for i in input_file.readline().split(",")]
    boards = []
    
    while True:
        line = input_file.readline()
        
        if not line:
            break

        board = []
        for i in range(BINGO_DIM):
            line = [int(char) for char in input_file.readline().split()]
            board.append(line)
        boards.append(board)
    input_file.close()
    return inputs, boards

def p1():
    inputs, boards = process_bingo_input('input/day04_test')
    print(inputs)

    boards_marked = []
    for i, board in enumerate(boards):
        boards_marked.append(
            [
                ['' for x in range(BINGO_DIM)]
                for y in range(BINGO_DIM)
            ]
        )

    for num in inputs:
        # print(num)
        # go through each board, mark boards_marked if it's a match
        for board_idx, board in enumerate(boards):
            for x, row in enumerate(board):
                for y, cell in enumerate(row):
                    if cell == num:
                        boards_marked[board_idx][x][y] = 'X'

        # TODO: check for winner

    # for board in boards_marked:
    #     pprint(board)


p1()