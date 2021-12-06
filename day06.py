input_file = open('input/day06_full', 'r')
fish = [int(i) for i in input_file.readline().split(",")]

input_file.close()

NUM_DAYS = 80
# print(f"initial: {fish}")

for day in range(NUM_DAYS + 1):
    new_fish = [8 for fish_timer in fish if fish_timer < 0]
    fish = [6 if fish_timer < 0 else fish_timer for fish_timer in fish ]
    fish = [*fish, *new_fish]
    # print(f"after {day} day(s): {fish}")
    fish = [fish_timer - 1 for fish_timer in fish]

num_fish = len(fish)
print(f"p1: {num_fish}")