# Edit this file: implement solve_part1

def solve_part1(lines):
    width = 101
    height = 103
    seconds = 100
    
    quadrants = [0, 0, 0, 0]
    
    for line in lines:
        if not line.strip():
            continue
            
        # Parse line: p=46,91 v=80,-6
        parts = line.split()
        pos_part = parts[0][2:]  # Remove 'p='
        vel_part = parts[1][2:]  # Remove 'v='
        
        px, py = map(int, pos_part.split(','))
        vx, vy = map(int, vel_part.split(','))
        
        # Calculate final position after 100 seconds
        final_x = (px + vx * seconds) % width
        final_y = (py + vy * seconds) % height
        
        # Check if robot is in any quadrant (not on middle lines)
        if final_x != width // 2 and final_y != height // 2:
            x_quad = 0 if final_x < width // 2 else 1
            y_quad = 0 if final_y < height // 2 else 1
            quadrant_idx = y_quad * 2 + x_quad
            quadrants[quadrant_idx] += 1
    
    return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]

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

