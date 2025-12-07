# Edit this file: implement solve_part1

def solve_part1(lines):
    # Parse robots
    robots = []
    for line in lines:
        if not line.strip():
            continue
        parts = line.split()
        # p=0,4 v=3,-3
        p_part = parts[0][2:]  # remove "p="
        v_part = parts[1][2:]  # remove "v="
        px, py = map(int, p_part.split(','))
        vx, vy = map(int, v_part.split(','))
        robots.append(((px, py), (vx, vy)))
    
    # Simulate 100 seconds
    width, height = 101, 103
    for _ in range(100):
        new_robots = []
        for (px, py), (vx, vy) in robots:
            px = (px + vx) % width
            py = (py + vy) % height
            new_robots.append(((px, py), (vx, vy)))
        robots = new_robots
    
    # Count robots in each quadrant
    # Middle lines are at width//2 and height//2 (index 50 and 51)
    mid_x = width // 2  # 50
    mid_y = height // 2  # 51
    
    q1 = q2 = q3 = q4 = 0
    for (px, py), _ in robots:
        if px == mid_x or py == mid_y:
            continue
        if px < mid_x and py < mid_y:
            q1 += 1
        elif px > mid_x and py < mid_y:
            q2 += 1
        elif px < mid_x and py > mid_y:
            q3 += 1
        elif px > mid_x and py > mid_y:
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

