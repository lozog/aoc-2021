from collections import defaultdict
from pprint import pprint
import re

input_file = open("input/day14_full", 'r')
template = input_file.readline().strip()
input_file.readline() # skip empty line of input
data = input_file.read().splitlines()

rules = defaultdict(lambda: None)
for line in data:
    # print(line)

    # regex for AB -> C
    res = re.search("([A-Z][A-Z])\ \-\>\ ([A-Z])", line)

    pair = res.group(1)
    insert = res.group(2)
    # print(pair, insert)

    rules[pair] = insert

input_file.close()

rules = dict(rules)
# pprint(rules)

def get_occurrences(polymer):
    occurrences = defaultdict(lambda: 0)
    last_index = len(polymer) - 1
    for i, char in enumerate(polymer):
        if i == last_index:
            break
        needle = f"{char}{polymer[i+1]}"
        occurrences[needle] += 1
    return occurrences

NUM_STEPS = 40

occurrences = get_occurrences(template)
# pprint(dict(occurrences))
for step in range(NUM_STEPS):
    print(step)
    new_occurrences = defaultdict(lambda: 0)

    for pair, count in occurrences.items():
        rule = rules[pair]
        if rule is not None:
            new_occurrences[f"{pair[0]}{rule}"] += count
            new_occurrences[f"{rule}{pair[1]}"] += count
    occurrences = new_occurrences


# pprint(dict(occurrences))
letter_count = defaultdict(lambda: 0)
for pair, count in occurrences.items():
    letter_count[pair[0]] += count
    letter_count[pair[1]] += count

for letter in letter_count.keys():
    if letter == template[0]:
        letter_count[letter] += 1
    elif letter == template[-1]:
        letter_count[letter] += 1
    letter_count[letter] = int(letter_count[letter] / 2)

pprint(dict(letter_count))

most_common_count = max(letter_count.values())
least_common_count = min(letter_count.values())

# print(most_common_count)
# print(least_common_count)
res = most_common_count - least_common_count
print(res)