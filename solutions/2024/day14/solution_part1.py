# Edit this file: implement solve_part1

def solve_part1(lines):
    # Parse input
    robots = []
    for line in lines:
        if not line.strip():
            continue
        parts = line.split()
        p_part = parts[0].replace('p=', '')
        v_part = parts[1].replace('v=', '')
        px, py = map(int, p_part.split(','))
        vx, vy = map(int, v_part.split(','))
        robots.append(((px, py), (vx, vy)))
    
    # Dimensions for the actual puzzle
    width = 101
    height = 103
    seconds = 100
    
    # Calculate positions after 100 seconds
    quadrants = [0, 0, 0, 0]  # top-left, top-right, bottom-left, bottom-right
    
    for (px, py), (vx, vy) in robots:
        # Calculate new position after 100 seconds
        new_px = (px + vx * seconds) % width
        new_py = (py + vy * seconds) % height
        
        # Skip robots exactly in the middle
        mid_x = width // 2
        mid_y = height // 2
        
        if new_px == mid_x or new_py == mid_y:
            continue
            
        # Determine which quadrant
        if new_px < mid_x and new_py < mid_y:
            quadrants[0] += 1  # top-left
        elif new_px > mid_x and new_py < mid_y:
            quadrants[1] += 1  # top-right
        elif new_px < mid_x and new_py > mid_y:
            quadrants[2] += 1  # bottom-left
        elif new_px > mid_x and new_py > mid_y:
            quadrants[3] += 1  # bottom-right
    
    # Calculate safety factor
    result = 1
    for count in quadrants:
        result *= count
    
    return result

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples.
samples = [
    ("""p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3""", 12)
]  # TODO: fill with actual samples and expected results

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part1(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 1: {sample_result} ----") # YOU MUST NOT change this output format

# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part1(lines)
print(f"---- Final result Part 1: {final_result} ----") # YOU MUST NOT change this output format

