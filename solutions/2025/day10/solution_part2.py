import re
from collections import Counter

def solve_machine_joltage(joltage_requirements, buttons):
    """
    Solve for minimum button presses to reach joltage requirements.
    Uses a greedy approach with constraint solving.
    """
    num_counters = len(joltage_requirements)
    if num_counters == 0:
        return 0
    
    # Filter out counters with 0 requirement
    non_zero_indices = [i for i, req in enumerate(joltage_requirements) if req > 0]
    if not non_zero_indices:
        return 0
    
    # Work with only non-zero counters
    filtered_requirements = [joltage_requirements[i] for i in non_zero_indices]
    filtered_buttons = []
    for button in buttons:
        filtered_indices = []
        for idx in button:
            if idx in non_zero_indices:
                filtered_indices.append(non_zero_indices.index(idx))
        if filtered_indices:
            filtered_buttons.append(filtered_indices)
    
    if not filtered_buttons:
        return sum(filtered_requirements)
    
    # Use a more efficient approach: solve as a linear system
    # This is essentially a minimum-cost flow problem
    
    # First, try a greedy approach: use buttons that cover the most needed counters
    remaining = list(filtered_requirements)
    total_presses = 0
    
    # While we still have counters to reach
    while any(remaining):
        # Find the button that gives us the best "bang for buck"
        best_button = None
        best_score = -1
        
        for button in filtered_buttons:
            # Count how many counters this button can help with
            useful_count = 0
            for idx in button:
                if remaining[idx] > 0:
                    useful_count += 1
            
            # Score is based on usefulness and button size
            if useful_count > 0:
                score = useful_count / len(button)
                if score > best_score:
                    best_score = score
                    best_button = button
        
        if best_button is None:
            # If no button is useful, we're stuck - this shouldn't happen
            break
        
        # Determine how many times to press this button
        # We can't exceed any remaining requirement
        max_presses = min(remaining[idx] for idx in best_button if remaining[idx] > 0)
        
        # Press the button
        for _ in range(max_presses):
            for idx in best_button:
                if remaining[idx] > 0:
                    remaining[idx] -= 1
            total_presses += 1
    
    return total_presses

def solve_part2(lines):
    total_presses = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Extract joltage requirements in curly braces
        joltage_match = re.search(r'\{([^}]+)\}', line)
        if not joltage_match:
            continue
        joltage_str = joltage_match.group(1)
        joltage_requirements = list(map(int, joltage_str.split(',')))
        
        # Find all button wiring schematics in parentheses
        button_matches = re.findall(r'\(([^)]+)\)', line)
        buttons = []
        for btn in button_matches:
            if btn.strip():
                indices = list(map(int, btn.split(',')))
                buttons.append(indices)
        
        if not buttons or not joltage_requirements:
            continue
            
        # Solve for minimum presses
        machine_presses = solve_machine_joltage(joltage_requirements, buttons)
        total_presses += machine_presses
    
    return total_presses

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples IF there are any samples given for part 2.
samples = [
    ("""[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}""", 33)
]

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part2(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 2: {sample_result} ----") # YOU MUST NOT change this output format
# print(f"---- Sample NONE result Part 2: NONE ----") # Uncomment this if no samples are given for part 2
# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part2(lines)
print(f"---- Final result Part 2: {final_result} ----") # YOU MUST NOT change this output format
