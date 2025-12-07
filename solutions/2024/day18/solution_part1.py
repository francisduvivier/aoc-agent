from collections import deque

def solve_part1(lines):
    # Parse coordinates
    bytes = []
    for line in lines:
        x, y = map(int, line.split(','))
        bytes.append((x, y))
    
    # Simulate first 1024 bytes falling
    grid_size = 71
    grid = [[False] * grid_size for _ in range(grid_size)]
    
    for i in range(1024):
        x, y = bytes[i]
        grid[y][x] = True  # True means corrupted
    
    # BFS to find shortest path
    start = (0, 0)
    end = (70, 70)
    
    queue = deque([(start[0], start[1], 0)])  # (x, y, steps)
    visited = {start}
    
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    while queue:
        x, y, steps = queue.popleft()
        
        if (x, y) == end:
            return steps
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            if 0 <= nx < grid_size and 0 <= ny < grid_size:
                if not grid[ny][nx] and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny, steps + 1))
    
    return -1  # No path found

# Sample data - may contain multiple samples from the problem statement.
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
