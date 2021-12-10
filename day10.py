input_file = open('input/day10_full', 'r')
data = input_file.read().splitlines()
input_file.close()

pairs = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

error_points = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}

completion_points = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4
}

def calc_error_score(line):
    stack = []
    for char in line:
        if char in ["(", "[", "{", "<"]:
            stack.append(char)
        else:
            current_char = stack.pop()
            if char != pairs[current_char]:
                return error_points[char]
    return 0

def complete_line(line):
    stack = []
    for char in line:
        if char in ["(", "[", "{", "<"]:
            stack.append(char)
        else:
            current_char = stack.pop()
    return ''.join([pairs[c] for c in stack[::-1]])

def p1():
    total_error_score = sum([calc_error_score(line) for line in data])
    print(f"p1: {total_error_score}")

def p2():
    error_scores = [calc_error_score(line) for line in data]
    incomplete_lines = [line for i, line in enumerate(data) if error_scores[i] == 0] # discard corrupted lines
    scores = []
    for line in incomplete_lines:
        score = 0
        for char in complete_line(line):
            score = score * 5 + completion_points[char]
        scores.append(score)
    res = sorted(scores)[int(len(scores) / 2)]
    print(f"p2: {res}")

p2()