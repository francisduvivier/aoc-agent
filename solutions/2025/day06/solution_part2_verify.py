def solve_part2(lines):
    # Find the width of the worksheet
    width = max(len(line) for line in lines)
    
    # Pad all lines to the same width
    for i in range(len(lines)):
        lines[i] = lines[i].ljust(width)
    
    # Identify problem boundaries by finding columns of only spaces
    problem_boundaries = []
    col_idx = 0
    
    while col_idx < width:
        # Skip spaces
        while col_idx < width and lines[0][col_idx] == ' ':
            col_idx += 1
        
        if col_idx >= width:
            break
            
        start_col = col_idx
        
        # Find the end of this problem (next column of only spaces)
        while col_idx < width and not all(lines[row_idx][col_idx] == ' ' for row_idx in range(len(lines))):
            col_idx += 1
            
        end_col = col_idx - 1
        problem_boundaries.append((start_col, end_col))
    
    total = 0
    
    # Process each problem from right to left
    for start_col, end_col in reversed(problem_boundaries):
        # Extract the operator from the bottom row
        operator = lines[-1][start_col]
        
        # Extract numbers from each column in this problem
        numbers = []
        
        for col_idx in range(start_col, end_col + 1):
            # Build the number from top to bottom
            num_str = ""
            for row_idx in range(len(lines) - 1):  # Exclude the operator row
                char = lines[row_idx][col_idx]
                if char != ' ':
                    num_str += char
            
            if num_str:  # Only process if we found digits
                numbers.append(int(num_str))
        
        # Calculate the result for this problem
        if operator == '+':
            result = sum(numbers)
        elif operator == '*':
            result = 1
            for num in numbers:
                result *= num
        
        total += result
    
    return total

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples IF there are any samples given for part 2.
samples = [
    ("123 328  51 64\n 45 64  387 23\n  6 98  215 314\n*   +   *   +", 3263827)
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
