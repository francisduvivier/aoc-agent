def is_safe(levels):
    """Check if a report is safe according to the rules."""
    if len(levels) < 2:
        return True
    
    # Determine if increasing or decreasing
    if levels[0] < levels[1]:
        # Increasing
        for i in range(1, len(levels)):
            diff = levels[i] - levels[i-1]
            if diff < 1 or diff > 3:
                return False
    elif levels[0] > levels[1]:
        # Decreasing
        for i in range(1, len(levels)):
            diff = levels[i-1] - levels[i]
            if diff < 1 or diff > 3:
                return False
    else:
        # Equal adjacent levels
        return False
    
    return True

def solve_part2(lines):
    """Count safe reports allowing removal of one level."""
    safe_count = 0
    
    for line in lines:
        levels = list(map(int, line.split()))
        
        # Check if already safe
        if is_safe(levels):
            safe_count += 1
            continue
        
        # Try removing each level and check if any makes it safe
        for i in range(len(levels)):
            modified_levels = levels[:i] + levels[i+1:]
            if is_safe(modified_levels):
                safe_count += 1
                break
    
    return safe_count

# Sample data from problem statement
samples = [
    ("""7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9""", 4)
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
