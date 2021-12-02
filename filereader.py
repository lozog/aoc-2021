DEBUG = True

def log(input_str):
    if DEBUG:
        print(input_str)


input_file = open('day02_input_test.txt', 'r')

while True:
    line = input_file.readline()

    if not line:
        break

    log(line)
input_file.close()
