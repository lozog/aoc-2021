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
            # each cell on the board will be a length-2 list: [number, marked]
            # marked == 1 if number has been called, else 0
            line = [[int(char), 0] for char in input_file.readline().split()]
            board.append(line)
        boards.append(board)
    input_file.close()
    return inputs, boards

def find_winner(boards):
    """
    returns index of winning board
    or None if none are winning
    """
    for board_idx, board in enumerate(boards):
        # check rows
        for x, row in enumerate(board):
            if sum([cell[1] for cell in row]) == BINGO_DIM:
                return board_idx

        # check columns
        board_transposed = list(zip(*board))
        for x, row in enumerate(board_transposed):
            if sum([cell[1] for cell in row]) == BINGO_DIM:
                return board_idx

    return None

def p1():
    inputs, boards = process_bingo_input('input/day04_full')
    # print(inputs)
    last_num = None

    for input_num in inputs:
        # print(input_num)
        last_num = input_num
        # go through each board, mark boards_marked if it's a match
        for board_idx, board in enumerate(boards):
            for x, row in enumerate(board):
                for y, cell in enumerate(row):
                    if cell[0] == input_num:
                        cell[1] = 1

        winner_idx = find_winner(boards)

        if winner_idx:
            break

    # assuming we have a winner_idx
    print(f"winner: {winner_idx}")

    # find winner score
    winner = boards[winner_idx]
    sum_of_unmarked_cells = 0
    for row in winner:
        for cell in row:
            if cell[1] == 0:
                sum_of_unmarked_cells += cell[0]
    print(f"p1: {sum_of_unmarked_cells * input_num}")

p1()