# Edit this file: implement solve_part2

def solve_part2(lines):
    position = 50
    count = 0
    for line in lines:
        if not line:
            continue
        dir = line[0]
        steps = int(line[1:])
        for _ in range(steps):
            if dir == 'R':
                position = (position + 1) % 100
            else:
                position = (position - 1) % 100
            if position == 0:
                count += 1
    return count

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples IF there are any samples given for part 2.
samples = [("L68\nL30\nR48\nL5\nR60\nL55\nL1\nL99\nR14\nL82", 6)]  # TODO: fill with actual samples and expected results

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part2(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 2: {sample_result} ----") # YOU MUST NOT change this output format
# print(f"---- Sample NONE result Part 2: NONE ----") # Uncomment this if no samples are given for part 2
# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part2(lines)
print(f"---- Final result Part 2: {final_result} ----") # YOU MUST NOT change this output format
