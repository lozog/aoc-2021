from math import floor
from statistics import mean, median

input_file = open('input/day07_full', 'r')
crabs = [int(i) for i in input_file.readline().split(",")]
input_file.close()

median = floor(median(crabs))
mean = floor(mean(crabs))

fuel_spent = sum([abs(c - median) for c in crabs]) # p1
print(f"p1: {fuel_spent}")

def sum_from_1_to_n(n: int):
    # returns sum of 1 + 2 + ... + abs(n)
    if n == 0:
        return 0
    n = abs(n)
    return int((n/2) * (1 + n))

fuel_spent = sum([sum_from_1_to_n(c - mean) for c in crabs]) # p2

print(f"p2: {fuel_spent}")
