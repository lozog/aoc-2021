from pprint import pprint

input_file = open('input/day06_full', 'r')
fish = [int(i) for i in input_file.readline().split(",")]
input_file.close()

NUM_DAYS = 256

# keys are days left until next spawn (aka timer), values are # of fish at that timer value
fish_map = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0}

for fish_timer in fish:
    fish_map[fish_timer] += 1
# pprint(fish_map)

for day in range(NUM_DAYS):
    num_fish_at_0 = 0
    for timer, fish_count in fish_map.items(): # shift all fish down one spot (i.e. decrement timer for each)
        if timer == 0:
            num_fish_at_0 = fish_count
        else:
            fish_map[timer - 1] = fish_count

    fish_map[6] += num_fish_at_0
    fish_map[8] = num_fish_at_0
# print(fish_map)

print(sum(fish_map.values()))
