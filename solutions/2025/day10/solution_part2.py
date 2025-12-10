import re
from collections import deque

def solve_part2(lines):
    total_presses = 0
    for line in lines:
        # Parse the line
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
        
        # Solve for minimum presses using BFS
        # State is a tuple of current counter values
        num_counters = len(joltage_requirements)
        start_state = tuple(0 for _ in range(num_counters))
        target_state = tuple(joltage_requirements)
        
        # BFS queue: (state, presses_so_far)
        queue = deque([(start_state, 0)])
        visited = {start_state}
        
        min_presses = None
        
        while queue:
            state, presses = queue.popleft()
            
            # Check if we reached the target
            if state == target_state:
                min_presses = presses
                break
            
            # Try pressing each button
            for button in buttons:
                # Create new state by adding 1 to each counter affected by this button
                new_state_list = list(state)
                for counter_idx in button:
                    new_state_list[counter_idx] += 1
                new_state = tuple(new_state_list)
                
                # Skip if we've already visited this state or if any counter exceeds target
                if new_state in visited:
                    continue
                
                # Pruning: if any counter exceeds the target, skip this state
                if any(new_state[i] > target_state[i] for i in range(num_counters)):
                    continue
                
                visited.add(new_state)
                queue.append((new_state, presses + 1))
        
        if min_presses is None:
            # Fallback: use sum of requirements (worst case)
            min_presses = sum(joltage_requirements)
        
        total_presses += min_presses
    
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
