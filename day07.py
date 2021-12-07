from statistics import median

input_file = open('input/day07_full', 'r')
crabs = [int(i) for i in input_file.readline().split(",")]
input_file.close()

# print(crabs)
median = int(median(crabs)) # TODO: do we want int? maybe floor or ceiling?
print(median)

fuel_spent = sum([abs(i - median) for i in crabs])

print(fuel_spent)