import re
from typing import List, Tuple

# Sample inputs and expected results from the problem statement
samples: List[Tuple[str, int]] = [
    (
        """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82""", 6
    )
]

def solve_part2(input_str: str) -> int:
    """
    Count the number of times the dial points at 0 during the sequence of rotations.
    This includes both times when the dial ends on 0 after a rotation and times when
    the dial passes through 0 during a rotation.
    """
    # Parse the input into a list of (direction, distance) tuples
    rotations = []
    for line in input_str.strip().split('\n'):
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
        
        # Count how many times the dial points at 0 during this rotation
        if direction == 'R':
            # Moving right (clockwise)
            if current_position < new_position:
                # No wrap-around
                if current_position < 0 <= new_position:
                    zero_count += 1
            else:
                # Wrap-around (crosses 99 -> 0)
                zero_count += 1
        else:
            # Moving left (counter-clockwise)
            if current_position > new_position:
                # No wrap-around
                if current_position > 0 >= new_position:
                    zero_count += 1
            else:
                # Wrap-around (crosses 0 -> 99)
                zero_count += 1
        
        # Check if the rotation ends on 0
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
    
    # Read and solve for the actual input
    try:
        with open('input.txt', 'r') as f:
            input_data = f.read()
        
        answer = solve_part2(input_data)
        print(f"---- Actual Answer Part 2: {answer} ----")
        
    except FileNotFoundError:
        print("Error: 'input.txt' not found in the current directory.")
    except Exception as e:
        print(f"Error reading input file: {e}")

if __name__ == "__main__":
    main()
