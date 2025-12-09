def solve_part1(input_lines, config):
    # Parse coordinates from input
    points = []
    for line in input_lines:
        line = line.strip()
        if not line:
            continue
        x, y = map(int, line.split(','))
        points.append((x, y))
    
    if len(points) < 2:
        return 0
    
    max_area = 0
    n = len(points)
    
    # Try all pairs of points as opposite corners
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = points[i]
            x2, y2 = points[j]
            
            # Calculate rectangle dimensions
            width = abs(x2 - x1)
            height = abs(y2 - y1)
            
            # Area is width * height
            area = width * height
            
            if area > max_area:
                max_area = area
    
    return max_area

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples.
samples = [
    (["7,1", "11,1", "11,7", "9,7", "9,5", "2,5", "2,3", "7,3"], 50)
]

for idx, (sample_input_lines, expected_result) in enumerate(samples, start=1):
    sample_config = "TODO"
    sample_result = solve_part1(sample_input_lines, sample_config)
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 1: {sample_result} ----") # YOU MUST NOT change this output format

# Run on the real puzzle input
final_config = "TODO"
final_result = solve_part1(open('input.txt').readlines(), final_config)
print(f"---- Final result Part 1: {final_result} ----") # YOU MUST NOT change this output format
