# Edit this file: implement solve_part2

def solve_part2(lines):
    stones = list(map(int, lines[0].split()))
    
    # Use memoization to avoid recalculating the same stone transformations
    memo = {}
    
    def transform_stone(stone, blinks_left):
        if blinks_left == 0:
            return 1
        
        key = (stone, blinks_left)
        if key in memo:
            return memo[key]
        
        if stone == 0:
            result = transform_stone(1, blinks_left - 1)
        else:
            s = str(stone)
            if len(s) % 2 == 0:
                mid = len(s) // 2
                left = int(s[:mid])
                right = int(s[mid:])
                result = transform_stone(left, blinks_left - 1) + transform_stone(right, blinks_left - 1)
            else:
                result = transform_stone(stone * 2024, blinks_left - 1)
        
        memo[key] = result
        return result
    
    total_stones = 0
    for stone in stones:
        total_stones += transform_stone(stone, 75)
    
    return total_stones

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples.
samples = [
    ("125 17", 537731)
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

