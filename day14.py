from collections import Counter, defaultdict
from pprint import pprint
import re

input_file = open("input/day14_full", 'r')
template = input_file.readline().strip()
input_file.readline() # skip empty line of input
data = input_file.read().splitlines()

rules = defaultdict(lambda: "")
for line in data:
    # print(line)

    # regex for AB -> C
    res = re.search("([A-Z][A-Z])\ \-\>\ ([A-Z])", line)

    pair = res.group(1)
    insert = res.group(2)
    # print(pair, insert)

    rules[pair] = insert

input_file.close()

# pprint(dict(rules))

NUM_STEPS = 10

new_polymer = template
for step in range(NUM_STEPS):
    last_index = len(new_polymer) - 1
    next_polymer = ""
    for i, char in enumerate(new_polymer):
        if i == last_index:
            next_polymer += char
            break
        needle = f"{char}{new_polymer[i+1]}"
        next_polymer += f"{char}{rules[needle]}"
    new_polymer = next_polymer
    # print(new_polymer)

most_common_count = Counter(list(new_polymer)).most_common()[0][1]
least_common_count = Counter(list(new_polymer)).most_common()[-1][1]

print(most_common_count)
print(least_common_count)
res = most_common_count - least_common_count
print(res)