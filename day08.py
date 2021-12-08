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

unique_segment_lengths = [2, 3, 4, 7]
unique_segment_count = 0
for pattern, output_values in signals:
    for output in output_values:
        if len(output) in unique_segment_lengths:
            unique_segment_count += 1

print(unique_segment_count)