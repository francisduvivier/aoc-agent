import sys
from typing import List, Tuple

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples.
samples = [
    (
        """3   4
4   3
2   5
1   3
3   9
3   3""",
        11
    )
]

def parse_input(lines: List[str]) -> Tuple[List[int], List[int]]:
    """Parse input lines into two lists of integers."""
    left_list = []
    right_list = []
    
    for line in lines:
        if not line.strip():
            continue
        
        # Split by whitespace and take the two numbers
        parts = line.strip().split()
        if len(parts) >= 2:
            left_list.append(int(parts[0]))
            right_list.append(int(parts[1]))
    
    return left_list, right_list

def solve_part1(lines: List[str]) -> int:
    """
    Solve part 1: Calculate the total distance between paired numbers.
    
    Pair up the smallest number in the left list with the smallest number in the right list,
    then the second-smallest left number with the second-smallest right number, and so on.
    Calculate the distance (absolute difference) for each pair and sum them up.
    """
    left_list, right_list = parse_input(lines)
    
    # Sort both lists
    left_list.sort()
    right_list.sort()
    
    # Calculate total distance
    total_distance = 0
    for left_val, right_val in zip(left_list, right_list):
        total_distance += abs(left_val - right_val)
    
    return total_distance

# Test with samples first
for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_res = solve_part1(sample_input.strip().splitlines())
    assert sample_res == expected_result, f"Sample {idx} result {sample_res} does not match expected {expected_result}"
    print(f"---- Sample {idx} Solution Part 1: {sample_res} ----")

# Run on the real puzzle input
try:
    with open('input.txt') as f:
        lines = [line.strip() for line in f]
    final_result = solve_part1(lines)
    print(f"---- Final Solution Part 1: {final_result} ----")
except FileNotFoundError:
    print("Error: input.txt not found in current directory")
    sys.exit(1)
except Exception as e:
    print(f"Error reading input: {e}")
    sys.exit(1)
