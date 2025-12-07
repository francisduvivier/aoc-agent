# Edit this file: implement solve_part1

def solve_part1(lines):
    # Parse robots: p=x,y v=dx,dy
    robots = []
    for line in lines:
        if not line.strip():
            continue
        # Extract numbers from "p=0,4 v=3,-3"
        parts = line.split()
        p_part = parts[0][2:]  # Remove "p="
        v_part = parts[1][2:]  # Remove "v="
        px, py = map(int, p_part.split(","))
        vx, vy = map(int, v_part.split(","))
        robots.append(((px, py), (vx, vy)))
    
    # Grid dimensions
    W = 101
    H = 103
    seconds = 100
    
    # Compute final positions after 100 seconds
    grid = [[0] * W for _ in range(H)]
    for (px, py), (vx, vy) in robots:
        fx = (px + vx * seconds) % W
        fy = (py + vy * seconds) % H
        grid[fy][fx] += 1
    
    # Count robots in each quadrant
    # Quadrants: top-left, top-right, bottom-left, bottom-right
    # Middle rows/cols (W//2 or H//2) are excluded
    mid_x = W // 2
    mid_y = H // 2
    
    q1 = q2 = q3 = q4 = 0
    for y in range(H):
        for x in range(W):
            if x == mid_x or y == mid_y:
                continue
            if x < mid_x and y < mid_y:
                q1 += grid[y][x]
            elif x > mid_x and y < mid_y:
                q2 += grid[y][x]
            elif x < mid_x and y > mid_y:
                q3 += grid[y][x]
            elif x > mid_x and y > mid_y:
                q4 += grid[y][x]
    
    return q1 * q2 * q3 * q4

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples.
samples = [
    (
        """p=0,4 v=3,-3
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
p=9,5 v=-3,-3""",
        12
    )
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

