# Edit this file: implement solve_part2

def solve_part2(lines):
    stones = list(map(int, lines[0].split()))
    
    # Use memoization to avoid recalculating the same subproblems
    memo = {}
    
    def count_stones(stone, blinks_left):
        if blinks_left == 0:
            return 1
        
        if (stone, blinks_left) in memo:
            return memo[(stone, blinks_left)]
        
        result = 0
        
        if stone == 0:
            # Rule 1: 0 becomes 1
            result = count_stones(1, blinks_left - 1)
        else:
            # Convert to string to check digit count
            stone_str = str(stone)
            if len(stone_str) % 2 == 0:
                # Rule 2: Even number of digits - split in half
                mid = len(stone_str) // 2
                left_half = int(stone_str[:mid])
                right_half = int(stone_str[mid:])
                result = count_stones(left_half, blinks_left - 1) + count_stones(right_half, blinks_left - 1)
            else:
                # Rule 3: Odd number of digits - multiply by 2024
                result = count_stones(stone * 2024, blinks_left - 1)
        
        memo[(stone, blinks_left)] = result
        return result
    
    total_stones = 0
    for stone in stones:
        total_stones += count_stones(stone, 75)
    
    return total_stones

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples.
samples = []  # TODO: fill with actual samples and expected results

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part2(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 2: {sample_result} ----") # YOU MUST NOT change this output format

# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part2(lines)
print(f"---- Final result Part 2: {final_result} ----") # YOU MUST NOT change this output format

