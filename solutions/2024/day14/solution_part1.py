# Edit this file: implement solve_part1

def solve_part1(lines):
    # Parse robots: p=x,y v=dx,dy
    robots = []
    for line in lines:
        if not line.strip():
            continue
        parts = line.split()
        p = parts[0][2:]  # remove "p="
        v = parts[1][2:]  # remove "v="
        x, y = map(int, p.split(","))
        dx, dy = map(int, v.split(","))
        robots.append((x, y, dx, dy))
    
    # Dimensions from problem: 101 wide, 103 tall
    W, H = 101, 103
    seconds = 100
    
    # Simulate 100 seconds
    counts = [0, 0, 0, 0]  # Q1, Q2, Q3, Q4
    mid_x = W // 2  # 50
    mid_y = H // 2  # 51
    
    for x, y, dx, dy in robots:
        nx = (x + dx * seconds) % W
        ny = (y + dy * seconds) % H
        
        # Skip if on middle lines
        if nx == mid_x or ny == mid_y:
            continue
            
        # Determine quadrant
        if nx < mid_x and ny < mid_y:
            counts[0] += 1  # top-left
        elif nx > mid_x and ny < mid_y:
            counts[1] += 1  # top-right
        elif nx < mid_x and ny > mid_y:
            counts[2] += 1  # bottom-left
        elif nx > mid_x and ny > mid_y:
            counts[3] += 1  # bottom-right
    
    return counts[0] * counts[1] * counts[2] * counts[3]

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

