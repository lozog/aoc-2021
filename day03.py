from pprint import pprint

def p1():

    input_file = open('input/day03_full', 'r')
    report = [list(line) for line in input_file.read().splitlines()] # 2d list of list of chars
    transposed_report = list(zip(*report)) # black magic
    num_diagnostics = len(report)

    gamma_rate = ""
    epsilon_rate = ""

    for column in transposed_report:
        num_ones = sum([int(i) for i in column])
        

        if num_ones > num_diagnostics / 2:
            gamma_rate += "1"
            epsilon_rate += "0"
        else:
            gamma_rate += "0"
            epsilon_rate += "1"

    print(gamma_rate, epsilon_rate)
    print(int(gamma_rate, 2) * int(epsilon_rate, 2))

p1()