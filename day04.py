from pprint import pprint

def process_bingo_input(file):
    """
    reads the input file and returns the list of bingo inputs
    and a list of boards, represented as 2D arrays
    """
    input_file = open(file, 'r')
    inputs = input_file.readline()
    boards = []
    
    while True:
        line = input_file.readline()
        
        if not line:
            break

        board = []
        for i in range(5):
            line = [char for char in input_file.readline().split()]
            board.append(line)
        boards.append(board)
    input_file.close()
    return inputs, boards

def p1():
    inputs, boards = process_bingo_input('input/day04_test')
    print(inputs)
    for board in boards:
        pprint(board)

p1()