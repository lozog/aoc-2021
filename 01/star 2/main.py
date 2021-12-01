input_file = open('../input_full.txt', 'r')

increase_count = 0
prev_window_sum = None
cur_window = list()
has_seen_first_window = False

while True:
    # Get next line from file
    line = input_file.readline()

    # if line is empty
    # end of file is reached
    if not line:
        break

    cur_window.append(int(line))

    if len(cur_window) > 3:
        cur_window.pop(0)

    if len(cur_window) == 3:
        cur_window_sum = sum(cur_window)
        print(f"cur_window: {cur_window}, sum: {cur_window_sum}")

        if prev_window_sum is not None:
            if cur_window_sum > prev_window_sum:
                print(f"{cur_window_sum} > {prev_window_sum}")
                increase_count += 1
            
        prev_window_sum = cur_window_sum
 
input_file.close()

print(f"increase_count: {increase_count}")