# Edit this file: implement solve_part1

def solve_part1(lines):
    left_list = []
    right_list = []
    
    for line in lines:
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) >= 2:
            left_list.append(int(parts[0]))
            right_list.append(int(parts[1]))
    
    left_list.sort()
    right_list.sort()
    
    total_distance = 0
    for left_val, right_val in zip(left_list, right_list):
        total_distance += abs(left_val - right_val)
    
    return total_distance

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples.
samples = [
    ("3   4\n4   3\n2   5\n1   3\n3   9\n3   3", 11)
]  # TODO: fill with actual samples and expected results

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part1(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 1: {sample_result} ----") # YOU MUST NOT change this output format

# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part1(lines)
print(f"---- Final result Part 1: {final_result} ----") # YOU MUST NOT change this output format
