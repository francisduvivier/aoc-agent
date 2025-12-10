import re
from collections import deque

def solve_machine_joltage(joltage_requirements, buttons):
    """
    Solve for minimum button presses to reach joltage requirements.
    Uses a more efficient approach with better pruning and heuristics.
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
    
    # Use BFS with better pruning
    start_state = tuple(0 for _ in filtered_requirements)
    target_state = tuple(filtered_requirements)
    
    # Priority queue for BFS
    queue = deque([(start_state, 0)])
    visited = {start_state}
    
    # Calculate a lower bound for the solution
    min_possible = max(filtered_requirements)
    
    while queue:
        state, presses = queue.popleft()
        
        if state == target_state:
            return presses
        
        # Try each button
        for button in filtered_buttons:
            new_state_list = list(state)
            for counter_idx in button:
                new_state_list[counter_idx] += 1
            new_state = tuple(new_state_list)
            
            if new_state in visited:
                continue
                
            # Pruning: if any counter exceeds target, skip
            if any(new_state[i] > target_state[i] for i in range(len(filtered_requirements))):
                continue
                
            # Pruning: if we've used too many presses already
            # Use a tighter bound: sum of remaining requirements divided by max button size
            remaining_presses_needed = sum(target_state[i] - new_state[i] for i in range(len(filtered_requirements)))
            if remaining_presses_needed == 0:
                return presses + 1
            
            max_button_size = max(len(btn) for btn in filtered_buttons)
            if presses + 1 + (remaining_presses_needed + max_button_size - 1) // max_button_size > sum(filtered_requirements):
                continue
                
            visited.add(new_state)
            queue.append((new_state, presses + 1))
    
    # Fallback: use sum of requirements
    return sum(filtered_requirements)

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
