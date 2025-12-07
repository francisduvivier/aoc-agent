# Edit this file: implement solve_part2

def solve_part2(lines):
    # Parse input
    patterns = lines[0].split(', ')
    designs = []
    for line in lines[2:]:
        if line:
            designs.append(line)
    
    # Count ways to make each design
    total_ways = 0
    for design in designs:
        ways = count_ways(design, patterns)
        total_ways += ways
    
    return total_ways

def count_ways(design, patterns):
    # DP approach: ways[i] = number of ways to make design[:i]
    ways = [0] * (len(design) + 1)
    ways[0] = 1  # Empty string can be made in 1 way
    
    for i in range(1, len(design) + 1):
        for pattern in patterns:
            if i >= len(pattern) and design[i-len(pattern):i] == pattern:
                ways[i] += ways[i-len(pattern)]
    
    return ways[len(design)]

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples IF there are any samples given for part 2.
samples = [
    ("r, wr, b, g, bwu, rb, gb, br\n\nbrwrr\nbggr\ngbbr\nrrbgbr\nubwu\nbwurrg\nbrgr\nbbrgwb", 16)
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

