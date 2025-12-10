import re
from collections import Counter
from itertools import product
import sys

def solve_machine_joltage(joltage_requirements, buttons):
    """
    Solve for minimum button presses to reach joltage requirements.
    Uses a more systematic approach with constraint satisfaction.
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
    
    num_counters = len(filtered_requirements)
    num_buttons = len(filtered_buttons)
    
    # Use a more systematic approach: try to find the minimal solution
    # We need to solve: A * x >= b, minimize sum(x)
    # where A[i][j] = 1 if button j affects counter i, 0 otherwise
    # and b[i] = requirement for counter i
    
    # Build the constraint matrix
    constraint_matrix = [[0] * num_buttons for _ in range(num_counters)]
    for button_idx, button in enumerate(filtered_buttons):
        for counter_idx in button:
            constraint_matrix[counter_idx][button_idx] = 1
    
    # Use a more sophisticated search algorithm
    # Start with a simple upper bound: press each button enough times
    # to satisfy its most demanding counter
    upper_bound = sum(filtered_requirements)
    
    # Try to find a better solution using a systematic search
    # For small instances, we can try all combinations up to a certain limit
    max_presses_per_button = max(filtered_requirements) + 1
    
    # Use a more efficient search: branch and bound
    best_solution = upper_bound
    
    def search(button_idx, current_presses, current_totals):
        nonlocal best_solution
        
        # If we've processed all buttons
        if button_idx == num_buttons:
            # Check if all requirements are satisfied
            if all(current_totals[i] >= filtered_requirements[i] for i in range(num_counters)):
                best_solution = min(best_solution, sum(current_presses))
            return
        
        # If we've already exceeded the best solution, prune
        if sum(current_presses) >= best_solution:
            return
        
        # Try different numbers of presses for this button
        # Calculate minimum presses needed for this button
        min_presses = 0
        for i in range(num_counters):
            if constraint_matrix[i][button_idx] > 0:
                remaining = max(0, filtered_requirements[i] - current_totals[i])
                if remaining > 0:
                    min_presses = max(min_presses, (remaining + constraint_matrix[i][button_idx] - 1) // constraint_matrix[i][button_idx])
        
        # Try from min_presses up to a reasonable upper bound
        max_presses = min(max_presses_per_button, best_solution - sum(current_presses))
        
        for presses in range(min_presses, max_presses + 1):
            # Update totals
            new_totals = current_totals[:]
            for i in range(num_counters):
                new_totals[i] += constraint_matrix[i][button_idx] * presses
            
            current_presses[button_idx] = presses
            search(button_idx + 1, current_presses, new_totals)
            current_presses[button_idx] = 0
    
    search(0, [0] * num_buttons, [0] * num_counters)
    
    return best_solution

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
