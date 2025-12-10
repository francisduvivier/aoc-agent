import re
from collections import Counter
from itertools import product
import sys

def solve_machine_joltage(joltage_requirements, buttons):
    """
    Solve for minimum button presses to reach joltage requirements.
    Uses a more efficient constraint-based approach.
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
    
    # Use a more efficient approach: solve using linear programming concepts
    # We want to minimize sum(x_i) subject to A * x >= b (since we can overshoot)
    # This is essentially a covering problem
    
    num_counters = len(filtered_requirements)
    num_buttons = len(filtered_buttons)
    
    # If we have exactly as many buttons as counters and they form a basis,
    # we can solve directly
    if num_buttons == num_counters:
        # Try to solve as a system of linear equations
        # This is a simplified approach for the specific problem structure
        pass
    
    # Use a greedy approach with backtracking
    # Start with the most efficient buttons (those that affect the most counters)
    button_efficiency = [(len(button), i) for i, button in enumerate(filtered_buttons)]
    button_efficiency.sort(reverse=True)
    
    # Try a more direct approach: use the fact that we can overshoot
    # We want to minimize total presses while satisfying all requirements
    
    # Use a simple but effective heuristic:
    # 1. For each counter, find buttons that can affect it
    # 2. Use the button that affects the most unsatisfied counters
    
    presses = [0] * num_buttons
    remaining = filtered_requirements[:]
    
    # Simple greedy algorithm that works well for this problem
    changed = True
    while changed and any(remaining):
        changed = False
        best_button = -1
        best_score = -1
        
        # Find the button that gives the best improvement
        for i, button in enumerate(filtered_buttons):
            # Score based on how many counters this button can help with
            score = 0
            can_help = False
            for idx in button:
                if remaining[idx] > 0:
                    score += remaining[idx]
                    can_help = True
            
            if can_help and score > best_score:
                best_score = score
                best_button = i
        
        if best_button >= 0:
            # Press this button once
            presses[best_button] += 1
            for idx in filtered_buttons[best_button]:
                if remaining[idx] > 0:
                    remaining[idx] -= 1
            changed = True
    
    # If we still have remaining requirements, use a fallback
    if any(remaining):
        # Add direct presses for remaining requirements
        for i, req in enumerate(remaining):
            if req > 0:
                # Find any button that affects this counter
                for button_idx, button in enumerate(filtered_buttons):
                    if i in button:
                        presses[button_idx] += req
                        break
    
    return sum(presses)

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
