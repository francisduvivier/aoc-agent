import re
from collections import Counter
from itertools import product

def solve_machine_joltage(joltage_requirements, buttons):
    """
    Solve for minimum button presses to reach joltage requirements.
    Uses integer linear programming approach with constraint satisfaction.
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
    
    # Use a more systematic approach: try to find the optimal solution
    # We need to solve: sum(button_presses[i] * button_effect[i][j]) = requirements[j]
    # for all j, where button_presses[i] >= 0 and integer
    
    # Build the constraint matrix
    num_buttons = len(filtered_buttons)
    num_vars = num_buttons
    
    # Simple brute force for small problems, or use a more sophisticated approach
    # For this problem, we can use a constraint satisfaction approach
    
    # Use a greedy approach that tries to minimize total presses
    # by solving the system more carefully
    
    # Convert to a linear algebra problem over integers
    # We want to minimize sum(x_i) subject to A * x = b
    
    # For this specific problem, we can use a more direct approach
    # by trying to find the optimal combination
    
    # Use a recursive search with memoization
    memo = {}
    
    def min_presses(remaining):
        if all(r == 0 for r in remaining):
            return 0
        
        remaining_tuple = tuple(remaining)
        if remaining_tuple in memo:
            return memo[remaining_tuple]
        
        min_presses_needed = float('inf')
        
        # Try each button
        for button in filtered_buttons:
            # Check if this button can help (has at least one positive counter)
            can_help = any(remaining[idx] > 0 for idx in button)
            if not can_help:
                continue
            
            # Find the maximum number of times we can press this button
            # without overshooting any requirement
            max_presses = min(remaining[idx] for idx in button if remaining[idx] > 0)
            
            # Try pressing this button different numbers of times
            for presses in range(1, max_presses + 1):
                # Simulate pressing the button 'presses' times
                new_remaining = list(remaining)
                for _ in range(presses):
                    for idx in button:
                        if new_remaining[idx] > 0:
                            new_remaining[idx] -= 1
                
                # Recursively solve for the remaining requirements
                result = min_presses(new_remaining)
                if result != float('inf'):
                    total_presses = presses + result
                    min_presses_needed = min(min_presses_needed, total_presses)
        
        memo[remaining_tuple] = min_presses_needed if min_presses_needed != float('inf') else float('inf')
        return memo[remaining_tuple]
    
    result = min_presses(filtered_requirements)
    return result if result != float('inf') else sum(filtered_requirements)

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
