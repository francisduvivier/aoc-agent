# Edit this file: implement solve_part1

def solve_part1(lines):
    # Parse input
    patterns = lines[0].split(', ')
    designs = lines[2:]
    
    # For each design, check if it can be made with available patterns
    possible_count = 0
    
    for design in designs:
        # Use dynamic programming to check if design is possible
        # dp[i] = True if first i characters of design can be formed
        dp = [False] * (len(design) + 1)
        dp[0] = True  # Empty string is always possible
        
        for i in range(1, len(design) + 1):
            for pattern in patterns:
                if (i >= len(pattern) and 
                    dp[i - len(pattern)] and 
                    design[i - len(pattern):i] == pattern):
                    dp[i] = True
                    break
        
        if dp[len(design)]:
            possible_count += 1
    
    return possible_count

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples.
samples = [
    ("""r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb""", 6)
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

