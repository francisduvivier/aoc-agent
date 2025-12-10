import re

def solve_part2(lines):
    total_presses = 0
    
    for line in lines:
        if not line.strip():
            continue
            
        # Parse the line
        # Format: [indicator] (button1) (button2) ... {joltages}
        
        # Extract buttons
        buttons = []
        button_matches = re.findall(r'\(([0-9,]+)\)', line)
        for match in button_matches:
            button = [int(x) for x in match.split(',')]
            buttons.append(button)
        
        # Extract joltage requirements
        joltage_match = re.search(r'\{([0-9,]+)\}', line)
        if joltage_match:
            targets = [int(x) for x in joltage_match.group(1).split(',')]
        else:
            continue
        
        # Find minimum button presses
        # This is an integer linear programming problem
        # We need to find non-negative integers x_i such that:
        # sum(x_i * button_i) = targets
        # and minimize sum(x_i)
        
        min_presses = find_min_presses(buttons, targets)
        total_presses += min_presses
    
    return total_presses

def find_min_presses(buttons, targets):
    # Use a greedy/search approach
    # Try to solve the system of linear equations
    n_counters = len(targets)
    n_buttons = len(buttons)
    
    # Build coefficient matrix
    # Each button affects certain counters
    matrix = [[0] * n_buttons for _ in range(n_counters)]
    
    for j, button in enumerate(buttons):
        for counter_idx in button:
            if counter_idx < n_counters:
                matrix[counter_idx][j] = 1
    
    # Try to find a solution using backtracking/search
    # For small problems, we can use brute force with pruning
    
    from itertools import product
    
    # Estimate upper bound for each button press
    max_presses = max(targets) * 2 if targets else 0
    
    # Try BFS/DFS to find minimum
    best = float('inf')
    
    # Use a more efficient search
    def search(button_presses, depth=0):
        nonlocal best
        
        if depth == n_buttons:
            # Check if we reached targets
            current = [0] * n_counters
            for j, presses in enumerate(button_presses):
                for counter_idx in buttons[j]:
                    if counter_idx < n_counters:
                        current[counter_idx] += presses
            
            if current == targets:
                total = sum(button_presses)
                best = min(best, total)
            return
        
        # Try different press counts for current button
        for presses in range(max_presses + 1):
            if sum(button_presses) + presses >= best:
                break
            search(button_presses + [presses], depth + 1)
    
    # For efficiency, use a smarter approach
    # Try to solve using Gaussian elimination for the minimum
    best = solve_linear_system(matrix, targets, n_buttons)
    
    return best if best != float('inf') else 0

def solve_linear_system(matrix, targets, n_buttons):
    # Simple brute force for small cases
    max_val = max(targets) if targets else 0
    max_presses = max_val * 2
    
    from itertools import product
    
    best = float('inf')
    
    # Limit search space
    for combo in product(range(min(max_presses + 1, 50)), repeat=n_buttons):
        result = [0] * len(targets)
        for j, presses in enumerate(combo):
            for i in range(len(targets)):
                result[i] += matrix[i][j] * presses
        
        if result == targets:
            best = min(best, sum(combo))
    
    return best

# Sample data
samples = [
    ("""[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}""", 33)
]

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part2(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 2: {sample_result} ----")

# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part2(lines)
print(f"---- Final result Part 2: {final_result} ----")
