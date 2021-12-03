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

# p1()

def p2():
    input_file = open('input/day03_full', 'r')

    report = [list(line) for line in input_file.read().splitlines()] # input as 2D array of chars
    # pprint(report)

    def most_common_digit(data, num_diagnostics):
        num_ones = sum([int(i) for i in data[0]])
        return int(num_ones >= (num_diagnostics / 2)) # shoutout to the C programming language

    def least_common_digit(data, num_diagnostics):
        num_ones = sum([int(i) for i in data[0]])
        return int(not num_ones >= (num_diagnostics / 2)) # shoutout to the C programming language

    oxygen_rating = ""
    co2_rating = ""

    for col in range(0, len(report[0])):
        filtered_report_oxygen = [row[col:] for row in report if col == 0 or ''.join(row[0:col]) == oxygen_rating]
        if (len(filtered_report_oxygen) == 1):
            oxygen_rating += filtered_report_oxygen[0][0]
        else:
            num_diagnostics = len(filtered_report_oxygen)
            transposed_report = list(zip(*filtered_report_oxygen))
            most_common_digit_in_col = most_common_digit(transposed_report, num_diagnostics)
            oxygen_rating += str(most_common_digit_in_col)

        filtered_report_co2 = [row[col:] for row in report if col == 0 or ''.join(row[0:col]) == co2_rating]
        if (len(filtered_report_co2) == 1):
            co2_rating += filtered_report_co2[0][0]
        else:
            num_diagnostics = len(filtered_report_co2)
            transposed_report = list(zip(*filtered_report_co2))
            least_common_digit_in_col = least_common_digit(transposed_report, num_diagnostics)
            co2_rating += str(least_common_digit_in_col)
        
    print(oxygen_rating, co2_rating)
    print(int(oxygen_rating, 2) * int(co2_rating, 2))
p2()