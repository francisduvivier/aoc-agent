from functools import cache

def solve_part2(lines):
    stones = list(map(int, lines[0].split()))
    
    @cache
    def process_stone(stone, blinks):
        if blinks == 0:
            return 1
        
        if stone == 0:
            return process_stone(1, blinks - 1)
        
        s = str(stone)
        if len(s) % 2 == 0:
            mid = len(s) // 2
            left = int(s[:mid])
            right = int(s[mid:])
            return process_stone(left, blinks - 1) + process_stone(right, blinks - 1)
        
        return process_stone(stone * 2024, blinks - 1)
    
    return sum(process_stone(stone, 75) for stone in stones)

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples.
samples = [
    ("125 17", 537731),
]  # TODO: fill with actual samples and expected results

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part2(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 2: {sample_result} ----") # YOU MUST NOT change this output format

# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part2(lines)
print(f"---- Final result Part 2: {final_result} ----") # YOU MUST NOT change this output format

