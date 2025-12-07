def solve_part1(lines):
    safe_count = 0
    for line in lines:
        levels = list(map(int, line.split()))
        
        # Check if all increasing or all decreasing
        is_increasing = all(1 <= levels[i+1] - levels[i] <= 3 for i in range(len(levels)-1))
        is_decreasing = all(1 <= levels[i] - levels[i+1] <= 3 for i in range(len(levels)-1))
        
        if is_increasing or is_decreasing:
            safe_count += 1
            
    return safe_count

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples.
samples = [
    ("""7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9""", 2)
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
