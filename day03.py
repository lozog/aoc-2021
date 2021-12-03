from pprint import pprint

def p1():

    input_file = open('input/day03_full', 'r')
    report = [list(line) for line in input_file.read().splitlines()] # input as 2D array of chars
    transposed_report = list(zip(*report)) # black magic to transpose array (i.e. swap rows & columns)
    num_diagnostics = len(report)

    gamma_rate = ""
    epsilon_rate = ""

    for column in transposed_report:
        num_ones = sum([int(i) for i in column])
        
        is_1_most_common_as_bool = 1 if num_ones > (num_diagnostics / 2) else 0 # shoutout to the C programming language
        gamma_rate += str(is_1_most_common_as_bool)
        epsilon_rate += str(1 - is_1_most_common_as_bool)

    # print(gamma_rate, epsilon_rate)
    print(int(gamma_rate, 2) * int(epsilon_rate, 2))

p1()