# Edit this file: implement solve_part2

def solve_part2(lines):
    position = 50
    count = 0
    
    for rotation in lines:
        direction = rotation[0]
        distance = int(rotation[1:])
        
        if direction == 'R':
            # Moving right (toward higher numbers)
            # Count how many times we pass 0 during this rotation
            # We pass 0 when we complete a full cycle
            # Calculate how many times we cross 0
            end_position = (position + distance) % 100
            # Number of times we pass 0 = number of full cycles
            count += (position + distance) // 100
            position = end_position
        else:  # direction == 'L'
            # Moving left (toward lower numbers)
            # Count how many times we pass 0 during this rotation
            end_position = (position - distance) % 100
            # When moving left, we pass 0 when going from 0 to 99
            # This happens when we cross the boundary
            if distance > position:
                # First pass through 0
                count += 1
                # After first pass, additional passes occur every 100 steps
                remaining = distance - position
                count += remaining // 100
            position = end_position
    
    return count

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples.
samples = [
    ("L68\nL30\nR48\nL5\nR60\nL55\nL1\nL99\nR14\nL82", 6)
]

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part2(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 2: {sample_result} ----")

# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part2(lines)
print(f"---- FINAL result Part 2: {final_result} ----")
