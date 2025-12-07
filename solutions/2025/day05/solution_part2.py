def solve_part2(lines):
    # Parse fresh ingredient ID ranges
    ranges = []
    for line in lines:
        if not line.strip():
            break
        start, end = map(int, line.split('-'))
        ranges.append((start, end))
    
    # Merge overlapping ranges
    ranges.sort()
    merged = []
    for start, end in ranges:
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    
    # Count total fresh ingredient IDs
    total_fresh = 0
    for start, end in merged:
        total_fresh += end - start + 1
    
    return total_fresh

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples IF there are any samples given for part 2.
samples = [
    ("""3-5
10-14
16-20
12-18

1
5
8
11
17
32""", 14)
]  # TODO: fill with actual samples and expected results

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
