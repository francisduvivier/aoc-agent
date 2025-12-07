# Edit this file: implement solve_part1

def solve_part1(lines):
    width = 101
    height = 103
    seconds = 100
    
    # Parse robots
    robots = []
    for line in lines:
        if not line.strip():
            continue
        parts = line.split()
        pos_part = parts[0][2:]  # Remove 'p='
        vel_part = parts[1][2:]  # Remove 'v='
        
        px, py = map(int, pos_part.split(','))
        vx, vy = map(int, vel_part.split(','))
        robots.append((px, py, vx, vy))
    
    # Simulate 100 seconds
    positions = []
    for px, py, vx, vy in robots:
        new_x = (px + vx * seconds) % width
        new_y = (py + vy * seconds) % height
        positions.append((new_x, new_y))
    
    # Count robots in each quadrant
    # Middle lines are at width//2 and height//2 (50 and 51)
    mid_x = width // 2  # 50
    mid_y = height // 2  # 51
    
    q1 = q2 = q3 = q4 = 0
    for x, y in positions:
        if x == mid_x or y == mid_y:
            continue  # Skip middle lines
        if x < mid_x and y < mid_y:
            q1 += 1
        elif x > mid_x and y < mid_y:
            q2 += 1
        elif x < mid_x and y > mid_y:
            q3 += 1
        elif x > mid_x and y > mid_y:
            q4 += 1
    
    return q1 * q2 * q3 * q4

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

