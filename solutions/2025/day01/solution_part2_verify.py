import re
from typing import List, Tuple

# Sample inputs and expected results from the problem statement
samples: List[Tuple[str, int]] = [
    ("""L68
L30
R48
L5
R60
L55
L1
L99
R14
L82""", 6)
]

def solve(input_str: str) -> int:
    """
    Solve the problem by counting the number of times the dial points at 0
    during or at the end of any rotation.
    """
    lines = input_str.strip().split('\n')
    
    # Parse the rotations
    rotations = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        match = re.match(r'([LR])(\d+)', line)
        if match:
            direction = match.group(1)
            distance = int(match.group(2))
            rotations.append((direction, distance))
    
    # Start at position 50
    current_pos = 50
    zero_count = 0
    
    # Process each rotation
    for direction, distance in rotations:
        # Count how many times we pass through 0 during this rotation
        if direction == 'R':
            # Moving right (toward higher numbers)
            # We pass through 0 if we cross from 99 to 0
            # Calculate the positions we'll visit
            for _ in range(distance):
                current_pos = (current_pos + 1) % 100
                if current_pos == 0:
                    zero_count += 1
        else:  # direction == 'L'
            # Moving left (toward lower numbers)
            # We pass through 0 if we cross from 0 to 99
            for _ in range(distance):
                current_pos = (current_pos - 1) % 100
                if current_pos == 0:
                    zero_count += 1
    
    return zero_count

# Test with samples first
for idx, (sample_input, expected) in enumerate(samples):
    result = solve(sample_input)
    print(f"---- Sample {idx + 1} Solution Part 2: {result} ----")
    assert result == expected, f"Expected {expected}, got {result}"

# Solve for actual input
try:
    with open('input.txt', 'r') as f:
        input_data = f.read()
    
    answer = solve(input_data)
    print(f"---- Actual Solution Part 2: {answer} ----")
except FileNotFoundError:
    print("Error: input.txt not found")
except Exception as e:
    print(f"Error reading input: {e}")
