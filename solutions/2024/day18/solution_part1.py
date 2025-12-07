# Edit this file: implement solve_part1

def solve_part1(lines):
    # Parse the input to get byte positions
    bytes = []
    for line in lines:
        x, y = map(int, line.split(','))
        bytes.append((x, y))
    
    # Create the grid (70x70)
    grid = [[False for _ in range(71)] for _ in range(71)]
    
    # Mark the first 1024 bytes as corrupted
    for i in range(1024):
        x, y = bytes[i]
        grid[y][x] = True  # True means corrupted
    
    # BFS to find shortest path
    from collections import deque
    
    queue = deque([(0, 0, 0)])  # (x, y, steps)
    visited = [[False for _ in range(71)] for _ in range(71)]
    visited[0][0] = True
    
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    while queue:
        x, y, steps = queue.popleft()
        
        if x == 70 and y == 70:
            return steps
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            if 0 <= nx <= 70 and 0 <= ny <= 70:
                if not visited[ny][nx] and not grid[ny][nx]:
                    visited[ny][nx] = True
                    queue.append((nx, ny, steps + 1))
    
    return -1  # No path found

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples.
samples = []  # TODO: fill with actual samples and expected results

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part1(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 1: {sample_result} ----") # YOU MUST NOT change this output format

# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part1(lines)
print(f"---- Final result Part 1: {final_result} ----") # YOU MUST NOT change this output format

