DEBUG = False

def log(*args):
    if DEBUG:
        print(args)

def p1():
    input_file = open('day02_input_full.txt', 'r')

    h_pos = 0
    depth = 0
    
    while True:
        line = input_file.readline()
        if not line:
            break

        command = line.split()
        direction = command[0]
        distance = int(command[1])
        log(direction, distance)

        if direction == "forward":
            h_pos += distance
        elif direction == "down":
            depth += distance
        elif direction == "up":
            depth -= distance

    input_file.close()

    log(h_pos, depth)
    res = h_pos * depth
    print(f"p1: {res}")
    
def p2():
    input_file = open('day02_input_full.txt', 'r')

    h_pos = 0
    depth = 0
    aim = 0

    while True:
        line = input_file.readline()
        if not line:
            break

        command = line.split()
        direction = command[0]
        distance = int(command[1])
        log(direction, distance)

        if direction == "forward":
            h_pos += distance
            depth += distance * aim
        elif direction == "down":
            aim += distance
        elif direction == "up":
            aim -= distance

    input_file.close()

    log(h_pos, depth)
    res = h_pos * depth
    print(f"p2: {res}")

p1()
p2()