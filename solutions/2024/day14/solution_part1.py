# Edit this file: implement solve_part1

def solve_part1(lines):
    # Parse input
    robots = []
    for line in lines:
        if not line.strip():
            continue
        # Format: p=x,y v=x,y
        parts = line.split()
        pos_part = parts[0][2:]  # Remove 'p='
        vel_part = parts[1][2:]  # Remove 'v='
        
        px, py = map(int, pos_part.split(','))
        vx, vy = map(int, vel_part.split(','))
        robots.append(((px, py), (vx, vy)))
    
    # Simulate 100 seconds
    width, height = 101, 103
    for _ in range(100):
        new_robots = []
        for (px, py), (vx, vy) in robots:
            new_px = (px + vx) % width
            new_py = (py + vy) % height
            new_robots.append(((new_px, new_py), (vx, vy)))
        robots = new_robots
    
    # Count robots in each quadrant
    # Quadrants are defined by splitting the grid in half (excluding middle lines)
    # Left half: x < width//2, Right half: x > width//2
    # Top half: y < height//2, Bottom half: y > height//2
    mid_x = width // 2
    mid_y = height // 2
    
    q1 = q2 = q3 = q4 = 0
    
    for (px, py), _ in robots:
        if px == mid_x or py == mid_y:
            continue  # Skip robots exactly in the middle
        
        if px < mid_x:
            if py < mid_y:
                q1 += 1  # Top-left
            else:
                q3 += 1  # Bottom-left
        else:  # px > mid_x
            if py < mid_y:
                q2 += 1  # Top-right
            else:
                q4 += 1  # Bottom-right
    
    return q1 * q2 * q3 * q4

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples.
samples = [
    ("p=0,4 v=3,-3\np=6,3 v=-1,-3\np=10,3 v=-1,2\np=2,0 v=2,-1\np=0,0 v=1,3\np=3,0 v=-2,-2\np=7,6 v=-1,-3\np=3,0 v=-1,-2\np=9,3 v=2,3\np=7,3 v=-1,2\np=2,4 v=2,-3\np=9,5 v=-3,-3", 12)
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

