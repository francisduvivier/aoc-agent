import re
from itertools import product

def solve_part2(lines):
    total_presses = 0
    for line in lines:
        # Parse the line
        # Extract indicator diagram (not used in part 2)
        # Extract buttons and joltage requirements
        # Format: [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
        
        # Find the joltage requirements in curly braces
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
        
        # Solve for minimum presses to achieve joltage requirements
        # This is a linear Diophantine problem: minimize sum(x_i) subject to A*x = b
        # where A[i][j] = 1 if button j affects counter i, else 0
        # and b[i] = joltage_requirements[i]
        
        num_counters = len(joltage_requirements)
        num_buttons = len(buttons)
        
        # Build the constraint matrix A
        A = [[0] * num_buttons for _ in range(num_counters)]
        for j, button in enumerate(buttons):
            for i in button:
                A[i][j] = 1
        
        # Try all possible combinations of button presses
        # Use a reasonable upper bound: sum of all joltage requirements
        max_presses = sum(joltage_requirements)
        min_presses = float('inf')
        
        # Use a more efficient approach: BFS or try to solve systematically
        # For now, use a bounded search
        # We can use a simple greedy approach or try small combinations first
        
        # Try combinations with increasing total presses
        for total in range(max_presses + 1):
            # Generate all combinations of button presses that sum to 'total'
            # This is equivalent to finding non-negative integer solutions to x_0 + x_1 + ... + x_n = total
            for combo in product(range(total + 1), repeat=num_buttons):
                if sum(combo) != total:
                    continue
                
                # Check if this combination satisfies the joltage requirements
                result = [0] * num_counters
                for j, presses in enumerate(combo):
                    for i in buttons[j]:
                        result[i] += presses
                
                if result == joltage_requirements:
                    min_presses = total
                    break
            
            if min_presses != float('inf'):
                break
        
        if min_presses == float('inf'):
            # Fallback: use a simple greedy approach
            # This shouldn't happen with the bounded search above
            min_presses = max_presses
        
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
