input_file = open('day02_input_test.txt', 'r')

while True:
    line = input_file.readline()

    if not line:
        break

    print(line)
input_file.close()
