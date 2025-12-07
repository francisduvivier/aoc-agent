from collections import deque

def solve_part1(lines):
    # Parse coordinates
    bytes = []
    for line in lines:
        if line.strip():
            x, y = map(int, line.strip().split(','))
            bytes.append((x, y))
    
    # Simulate first 1024 bytes falling
    grid_size = 70
    corrupted = set()
    for i in range(1024):
        corrupted.add(bytes[i])
    
    # BFS to find shortest path
    start = (0, 0)
    end = (grid_size, grid_size)
    
    queue = deque([(start[0], start[1], 0)])  # (x, y, steps)
    visited = {start}
    
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    while queue:
        x, y, steps = queue.popleft()
        
        if (x, y) == end:
            return steps
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            if 0 <= nx <= grid_size and 0 <= ny <= grid_size:
                if (nx, ny) not in corrupted and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny, steps + 1))
    
    return -1  # No path found

# Sample data from problem statement
samples = [
    """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0""".splitlines(), 22
]

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part1(sample_input)
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 1: {sample_result} ----")

# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part1(lines)
print(f"---- Final result Part 1: {final_result} ----")
