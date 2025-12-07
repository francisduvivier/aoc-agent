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
    Solve part 2 of the problem.
    
    Count the number of times the dial points at 0 during any rotation in the sequence.
    """
    lines = input_str.strip().split('\n')
    
    # Parse rotations
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
    
    for direction, distance in rotations:
        # Count how many times we pass through 0 during this rotation
        if direction == 'R':
            # Moving right (increasing numbers)
            # We pass through 0 if we cross the boundary from 99 to 0
            # Calculate final position
            final_pos = (current_pos + distance) % 100
            
            # Count how many times we hit 0
            # If we cross the boundary, we hit 0
            if current_pos + distance >= 100:
                # Calculate how many full cycles of 100 we make
                full_cycles = (current_pos + distance) // 100
                zero_count += full_cycles
            
            current_pos = final_pos
            
        else:  # direction == 'L'
            # Moving left (decreasing numbers)
            # We pass through 0 if we cross the boundary from 0 to 99
            # Calculate final position
            final_pos = (current_pos - distance) % 100
            
            # Count how many times we hit 0
            # If we cross the boundary, we hit 0
            if current_pos - distance < 0:
                # Calculate how many full cycles of 100 we make
                full_cycles = (distance - current_pos) // 100
                zero_count += full_cycles
                # If there's a remainder that crosses 0, add one more
                if (distance - current_pos) % 100 > 0:
                    zero_count += 1
            
            current_pos = final_pos
    
    return zero_count

# Test with samples first
for idx, (sample_input, expected) in enumerate(samples):
    sample_result = solve(sample_input)
    print(f"---- Sample {idx} Solution Part 2: {sample_result} ----")
    assert sample_result == expected, f"Expected {expected}, got {sample_result}"

# Now solve for the actual input
try:
    with open('input.txt', 'r') as f:
        input_data = f.read()
    
    result = solve(input_data)
    print(result)
except FileNotFoundError:
    print("input.txt not found, cannot solve for actual input")
except Exception as e:
    print(f"Error reading input: {e}")
