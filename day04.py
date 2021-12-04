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


def has_full_row(board):
    """
    returns True if board has a full marked row
    """
    for x, row in enumerate(board):
        if sum([cell[1] for cell in row]) == BINGO_DIM:
            return True
    return False


def find_winners(boards, found_winners=[]):
    """
    multiple boards can win at once!
    returns list of indices of winning boards
    or empty list if none are winning
    """
    new_winners = []
    for board_idx, board in enumerate(boards):
        if board_idx in found_winners or board_idx in new_winners:
            # skip boards that have already won
            continue

        # check rows
        if has_full_row(board):
            new_winners.append(board_idx)
            continue

        # check columns
        board_transposed = list(zip(*board))
        if has_full_row(board_transposed):
            new_winners.append(board_idx)
            continue

    return new_winners


def find_score(winner, last_num):
    sum_of_unmarked_cells = 0
    for row in winner:
        for cell in row:
            if cell[1] == 0:
                sum_of_unmarked_cells += cell[0]
    return sum_of_unmarked_cells * last_num


def apply_num(boards, input_num, found_winners=[]):
    """
    find every cell which matches input_num and set its second bit to 1
    """
    for board_idx, board in enumerate(boards):
        if board_idx in found_winners:
            # skip boards that have already won
            continue

        for row in board:
            for cell in row:
                if cell[0] == input_num:
                    cell[1] = 1
    return boards # Object references are passed by value. :smug_look:


def p1():
    inputs, boards = process_bingo_input('input/day04_full')

    for input_num in inputs:
        boards = apply_num(boards, input_num)
        winners = find_winners(boards)

        if len(winners) > 0:
            winner_idx = winners[0]
            break

    # assuming we have a winner_idx
    # print(f"winner: {winner_idx}")

    # find winner score
    score = find_score(boards[winner_idx], input_num)
    print(f"p1: {score}")
    
    return winner_idx


def p2():
    inputs, boards = process_bingo_input('input/day04_full')

    found_winners = []
    for input_num in inputs:
        boards = apply_num(boards, input_num, found_winners)
        winners = find_winners(boards, found_winners)

        if len(winners) > 0:
            found_winners = [*found_winners, *winners]
            last_winner_idx = winners[-1]

            if len(found_winners) == len(boards):
                # every board has won
                break

    last_winner = boards[last_winner_idx]
    last_winner_score = find_score(last_winner, input_num)
    print(f"p2: {last_winner_score}")

p1()
p2()