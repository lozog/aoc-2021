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

def find_winner(boards):
    """
    returns index of winning board
    or None if none are winning
    """
    for board_idx, board in enumerate(boards):
        # check rows
        for x, row in enumerate(board):
            if sum(row) == BINGO_DIM:
                return board_idx

        # check columns
        board_transposed = list(zip(*board))
        for x, row in enumerate(board_transposed):
            if sum(row) == BINGO_DIM:
                return board_idx

        # check diagonals
        diagonal_1 = [board[i][i] for i in range(len(board))] # from https://www.geeksforgeeks.org/python-print-diagonals-of-2d-list/
        if sum(diagonal_1) == BINGO_DIM:
            return board_idx
        diagonal_2 = [board[i][len(board)-1-i] for i in range(len(board))]
        if sum(diagonal_2) == BINGO_DIM:
            return board_idx

    return None


# testing find_winner
# loser = [[1,1,1,0,1],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
# row_winner = [[1,1,1,1,1],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
# col_winner = [[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0]]
# diag1_winner = [[1,0,0,0,0],[0,1,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1]]
# diag2_winner = deepcopy(diag1_winner)
# diag2_winner.reverse()

# res = find_winner([loser, diag2_winner])
# print(res)

def p1():
    inputs, boards = process_bingo_input('input/day04_test')
    print(inputs)

    boards_marked = []
    for i, board in enumerate(boards):
        boards_marked.append(
            [
                [0 for x in range(BINGO_DIM)]
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
                        boards_marked[board_idx][x][y] = 1

        winner = find_winner(boards_marked)

        if winner:
            break

    print(winner)
    for board in boards_marked:
        pprint(board)

p1()