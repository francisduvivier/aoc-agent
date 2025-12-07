from functools import lru_cache

def solve_part1(lines):
    stones = list(map(int, lines[0].split()))
    
    @lru_cache(maxsize=None)
    def transform(stone, blinks):
        if blinks == 0:
            return 1
        
        if stone == 0:
            return transform(1, blinks - 1)
        
        s = str(stone)
        if len(s) % 2 == 0:
            mid = len(s) // 2
            left = int(s[:mid])
            right = int(s[mid:])
            return transform(left, blinks - 1) + transform(right, blinks - 1)
        
        return transform(stone * 2024, blinks - 1)
    
    return sum(transform(stone, 25) for stone in stones)

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples.
samples = [
    ("125 17", 55312)
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
