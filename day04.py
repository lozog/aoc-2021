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

def find_score(winner, last_num):
    sum_of_unmarked_cells = 0
    for row in winner:
        for cell in row:
            if cell[1] == 0:
                sum_of_unmarked_cells += cell[0]
    return sum_of_unmarked_cells * last_num

def apply_num(boards, input_num):
    """
    find every cell which matches input_num and set its second bit to 1
    """
    for board in boards:
        for row in board:
            for cell in row:
                if cell[0] == input_num:
                    cell[1] = 1
    return boards # Object references are passed by value. :smug_look:

def p1():
    inputs, boards = process_bingo_input('input/day04_test')

    for input_num in inputs:
        boards = apply_num(boards, input_num)
        winner_idx = find_winner(boards)

        if winner_idx:
            break

    # assuming we have a winner_idx
    print(f"winner: {winner_idx}")

    # find winner score
    score = find_score(boards[winner_idx], input_num)
    print(f"p1: {score}")
    
    return winner_idx

p1()
