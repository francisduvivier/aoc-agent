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

def solve_part2(input_text: str) -> int:
    """
    Count the number of times the dial points at 0 during the sequence of rotations.
    This includes both times when the rotation ends at 0 and times when the dial passes 0 during a rotation.
    """
    # Parse the input into a list of (direction, distance) tuples
    rotations = []
    for line in input_text.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
        match = re.match(r'([LR])(\d+)', line)
        if match:
            direction = match.group(1)
            distance = int(match.group(2))
            rotations.append((direction, distance))
    
    current_position = 50
    zero_count = 0
    
    for direction, distance in rotations:
        # Calculate the new position after the rotation
        if direction == 'R':
            new_position = (current_position + distance) % 100
        else:  # direction == 'L'
            new_position = (current_position - distance) % 100
        
        # Count how many times the dial passes 0 during this rotation
        if direction == 'R':
            # Moving right: count how many times we cross 0
            if current_position < new_position:
                # No wrap-around, so we don't cross 0
                pass
            else:
                # Wrap-around: we cross 0 once
                zero_count += 1
        else:  # direction == 'L'
            # Moving left: count how many times we cross 0
            if current_position >= new_position:
                # No wrap-around, so we don't cross 0
                pass
            else:
                # Wrap-around: we cross 0 once
                zero_count += 1
        
        # If the rotation ends at 0, count that too
        if new_position == 0:
            zero_count += 1
        
        current_position = new_position
    
    return zero_count

def main():
    # Test with samples first
    for idx, (sample_input, expected) in enumerate(samples, 1):
        result = solve_part2(sample_input)
        print(f"---- Sample {idx} Solution Part 2: {result} ----")
        assert result == expected, f"Sample {idx} failed: expected {expected}, got {result}"
    
    # Read from input.txt and solve
    try:
        with open('input.txt', 'r') as f:
            input_data = f.read()
        
        answer = solve_part2(input_data)
        print(f"---- Final Answer Part 2: {answer} ----")
        
    except FileNotFoundError:
        print("Error: input.txt not found in current directory")
    except Exception as e:
        print(f"Error reading input: {e}")

if __name__ == "__main__":
    main()
