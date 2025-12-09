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
            width = abs(x2 - x1)
            height = abs(y2 - y1)
            area = width * height
            
            # Check if these two red tiles can serve as opposite corners
            # by verifying no other red tiles lie on the rectangle boundary
            valid = True
            
            # Check the other two corners of the rectangle
            corner1 = (x1, y2)
            corner2 = (x2, y1)
            
            # For these to be valid opposite corners, the other two corners
            # should NOT be red tiles (unless they're the same as our chosen corners)
            if corner1 in coords and corner1 != (x1, y1) and corner1 != (x2, y2):
                continue
            if corner2 in coords and corner2 != (x1, y1) and corner2 != (x2, y2):
                continue
            
            # Check edges of the rectangle (excluding corners)
            # Top edge (excluding corners)
            for x in range(min(x1, x2) + 1, max(x1, x2)):
                if (x, max(y1, y2)) in coords:
                    valid = False
                    break
            if not valid:
                continue
                
            # Bottom edge (excluding corners)
            for x in range(min(x1, x2) + 1, max(x1, x2)):
                if (x, min(y1, y2)) in coords:
                    valid = False
                    break
            if not valid:
                continue
                
            # Left edge (excluding corners)
            for y in range(min(y1, y2) + 1, max(y1, y2)):
                if (min(x1, x2), y) in coords:
                    valid = False
                    break
            if not valid:
                continue
                
            # Right edge (excluding corners)
            for y in range(min(y1, y2) + 1, max(y1, y2)):
                if (max(x1, x2), y) in coords:
                    valid = False
                    break
            if not valid:
                continue
            
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
