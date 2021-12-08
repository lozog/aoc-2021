input_file = open('input/day08_full', 'r')

signals = []
while True:
    line = input_file.readline()
    if not line:
        break
    line = line.split("|")

    patterns = line[0].split()
    output = line[1].split()
    signals.append((patterns, output))
input_file.close()

def p1():
    unique_segment_lengths = [2, 3, 4, 7]
    unique_segment_count = 0
    for pattern, output_values in signals:
        for output in output_values:
            if len(output) in unique_segment_lengths:
                unique_segment_count += 1

    print(f"p1: {unique_segment_count}")

def contains_all_chars(string_to_examine, chars_to_find):
    # returns true if every char of chars_to_find can be found in string_to_examine
    return len([c for c in string_to_examine if c in chars_to_find]) == len(chars_to_find)

def get_digit_from_key(digit_to_decode, digit_key):
    for i, digit in enumerate(digit_key):
        if digit == digit_to_decode:
            return i

total = 0
for pattern, output_values in signals:
    sorted_pattern = sorted(pattern, key=len) # it's easier if we look at them in order by length
    digit_key = ["" for i in range(10)] # when we find a digit, put its key here. e.g digit_key[0] == "ea" 1 is comprised of segments e and a
    for digit in sorted_pattern:
        digit = "".join(sorted(digit)) # we'll sort the digits lexicographically to make comparisons easier
        # print(f"{len(digit)}: {digit}")
        if len(digit) == 2: # 1
            digit_key[1] = digit
        elif len(digit) == 3: # 7
            digit_key[7] = digit
        elif len(digit) == 4: # 4
            digit_key[4] = digit
        elif len(digit) == 5: # 2, 3, 5
            if contains_all_chars(digit, digit_key[1]): # only 3 contains every segment in 1
                digit_key[3] = digit
                continue
            segment_diff = [c for c in digit if c not in digit_key[4]] # look at segments not shared with 4
            if len(segment_diff) == 2: # if there are 2 such segments, we have a 5
                digit_key[5] = digit
            else: # len == 3, meaning we have a 2
                digit_key[2] = digit
        elif len(digit) == 6:
            if contains_all_chars(digit, digit_key[3]): # only 9 contains every segment in 3
                digit_key[9] = digit
                continue
            segment_diff = [c for c in digit if c not in digit_key[7]] # look at segments not shared with 7
            if len(segment_diff) == 4: # if there are 4 such segments, we have a 6
                digit_key[6] = digit
            else: # len == 3, meaning we have a 0
                digit_key[0] = digit
        elif len(digit) == 7: # 8
            digit_key[8] = digit
    # print(sorted_pattern)
    # print(digit_key)

    res = []
    for digit_to_decode in output_values:
        digit_to_decode = "".join(sorted(digit_to_decode))
        # print(digit_to_decode)
        res.append(str(get_digit_from_key(digit_to_decode, digit_key)))
    # print(res)
    total += int("".join(res))
print(total)