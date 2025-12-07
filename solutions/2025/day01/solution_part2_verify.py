# Edit this file: implement solve_part2

def solve_part2(lines):
    position = 50
    count = 0
    
    for line in lines:
        direction = line[0]
        distance = int(line[1:])
        
        if direction == 'R':
            # Moving right (toward higher numbers)
            # Count how many times we pass 0 during this rotation
            new_position = (position + distance) % 100
            # We pass 0 if we wrap around from 99 to 0
            if position + distance >= 100:
                # Calculate how many full cycles of 100 we make
                count += (position + distance) // 100
            position = new_position
        else:  # direction == 'L'
            # Moving left (toward lower numbers)
            # Count how many times we pass 0 during this rotation
            new_position = (position - distance) % 100
            # We pass 0 if we wrap around from 0 to 99
            if position - distance < 0:
                # Calculate how many full cycles of 100 we make
                count += (distance - position) // 100
            position = new_position
        
        # Check if we end at 0
        if position == 0:
            count += 1
    
    return count

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples.
samples = [
    ("L68\nL30\nR48\nL5\nR60\nL55\nL1\nL99\nR14\nL82", 6)
]  # TODO: fill with actual samples and expected results

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part2(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 2: {sample_result} ----") # YOU MUST NOT change this output format

# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part2(lines)
print(f"---- FINAL result Part 2: {final_result} ----") # YOU MUST NOT change this output format

