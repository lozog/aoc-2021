input_file = open('input.txt', 'r')

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
        print(f"{line_num} > {prev_line} ?")
        if line_num > prev_line:
            increase_count += 1
            
    prev_line = line_num
 
input_file.close()

print(increase_count)