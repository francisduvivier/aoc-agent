import re

def solve_part2(lines):
    text = ''.join(lines)
    # Pattern to match do(), don't(), and mul(X,Y)
    pattern = r'(do\(\)|don\'t\(\)|mul\((\d{1,3}),(\d{1,3})\))'
    enabled = True
    total = 0
    
    for match in re.finditer(pattern, text):
        if match.group(1) == 'do()':
            enabled = True
        elif match.group(1) == "don't()":
            enabled = False
        else:
            # It's a mul instruction
            if enabled:
                x, y = int(match.group(2)), int(match.group(3))
                total += x * y
    
    return total

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples.
samples = [
    ("xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))", 48)
]

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part2(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 2: {sample_result} ----") # YOU MUST NOT change this output format

# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part2(lines)
print(f"---- Final result Part 2: {final_result} ----") # YOU MUST NOT change this output format
