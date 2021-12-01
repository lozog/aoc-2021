DEBUG = False

def log(input_str):
    if DEBUG:
        print(input_str)

def p1():
    input_file = open('input_full.txt', 'r')

    increase_count = 0
    prev_line = None

    while True:
        # Get next line from file
        line = input_file.readline()

        # if line is empty
        # end of file is reached
        if not line:
            break

        line_num = int(line)

        if prev_line is not None:
            if line_num > prev_line:
                increase_count += 1
                
        prev_line = line_num
    
    input_file.close()

    print(f"p1: increase_count: {increase_count}")

def p2():
    input_file = open('input_full.txt', 'r')
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
            log(f"cur_window: {cur_window}, sum: {cur_window_sum}")
    
            if prev_window_sum is not None:
                if cur_window_sum > prev_window_sum:
                    log(f"{cur_window_sum} > {prev_window_sum}")
                    increase_count += 1
                
            prev_window_sum = cur_window_sum
     
    input_file.close()
    
    print(f"p2: increase_count: {increase_count}")

p1()

p2()