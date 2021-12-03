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
        
        most_common_digit = int(num_ones > (num_diagnostics / 2)) # shoutout to the C programming language
        gamma_rate += str(most_common_digit)
        epsilon_rate += str(1 - most_common_digit)

    # print(gamma_rate, epsilon_rate)
    print(int(gamma_rate, 2) * int(epsilon_rate, 2))

p1()

def p2():
    input_file = open('input/day03_full', 'r')

    report = [list(line) for line in input_file.read().splitlines()] # input as 2D array of chars
    # pprint(report)

    def find_res(bit_criteria):
        res = ""
        for col in range(0, len(report[0])):
            filtered_report = [row[col:] for row in report if col == 0 or ''.join(row[0:col]) == res] # only look at rows whose first $col digits match res
            num_diagnostics = len(filtered_report)
            if (num_diagnostics == 1):
                # base case: if we only have one row left, that's the rest of the result
                return res + ''.join(filtered_report[0])
            else:
                transposed_report = list(zip(*filtered_report))
                num_ones = sum([int(i) for i in transposed_report[0]]) # count ones in first column
                res += str(int(bool(bit_criteria) == (num_ones >= (num_diagnostics / 2)))) # more black magic
        
        return res

    oxygen_rating = find_res(0)
    co2_rating = find_res(1)
        
    # print(oxygen_rating, co2_rating)
    print(int(oxygen_rating, 2) * int(co2_rating, 2))
p2()