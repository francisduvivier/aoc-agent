def solve_part1(input_lines, config):
    # Parse coordinates from input
    red_tiles = []
    for line in input_lines:
        line = line.strip()
        if line:
            x, y = map(int, line.split(','))
            red_tiles.append((x, y))
    
    # Find maximum area rectangle using any two red tiles as opposite corners
    max_area = 0
    n = len(red_tiles)
    
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = red_tiles[i]
            x2, y2 = red_tiles[j]
            
            # Calculate area of rectangle with these points as opposite corners
            area = abs(x2 - x1) * abs(y2 - y1)
            max_area = max(max_area, area)
    
    return max_area

# Sample data from the problem statement
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
    print(f"---- Sample {idx} result Part 1: {sample_result} ----")

# Run on the real puzzle input
final_config = "TODO"
final_result = solve_part1(open('input.txt').readlines(), final_config)
print(f"---- Final result Part 1: {final_result} ----")
