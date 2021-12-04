input_file = open('input/day04_test', 'r')

while True:
    line = input_file.readline()

    if not line:
        break

    print(line)
input_file.close()
