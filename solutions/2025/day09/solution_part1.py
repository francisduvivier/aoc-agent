# Edit this file: implement solve_part1

def solve_part1(input_lines, config):
    # Parse coordinates
    coords = []
    for line in input_lines:
        line = line.strip()
        if not line:
            continue
        x, y = map(int, line.split(','))
        coords.append((x, y))
    
    if not coords:
        return 0
    
    max_area = 0
    n = len(coords)
    
    # Try all pairs of red tiles as opposite corners
    for i in range(n):
        x1, y1 = coords[i]
        for j in range(i + 1, n):
            x2, y2 = coords[j]
            
            # Calculate rectangle area using these two points as opposite corners
            # The width is the difference in x coordinates + 1 (inclusive)
            # The height is the difference in y coordinates + 1 (inclusive)
            # We need to add 1 because we're counting the tiles themselves
            width = abs(x2 - x1) + 1
            height = abs(y2 - y1) + 1
            area = width * height
            
            # Update max area
            max_area = max(max_area, area)
    
    return max_area

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples.
samples = [
    ([
        "7,1",
        "11,1", 
        "11,7",
        "9,7",
        "9,5",
        "2,5",
        "2,3",
        "7,3"
    ], 50)
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
