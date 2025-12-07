import heapq

def solve_part1(lines):
    # Parse byte positions
    bytes = []
    for line in lines:
        x, y = map(int, line.split(','))
        bytes.append((x, y))
    
    # Simulate first 1024 bytes falling
    corrupted = set(bytes[:1024])
    
    # BFS/Dijkstra to find shortest path
    size = 70
    start = (0, 0)
    end = (size, size)
    
    # Priority queue: (distance, x, y)
    pq = [(0, start[0], start[1])]
    visited = set()
    
    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while pq:
        dist, x, y = heapq.heappop(pq)
        
        if (x, y) == end:
            return dist
            
        if (x, y) in visited:
            continue
            
        visited.add((x, y))
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            # Check bounds
            if 0 <= nx <= size and 0 <= ny <= size:
                if (nx, ny) not in visited and (nx, ny) not in corrupted:
                    heapq.heappush(pq, (dist + 1, nx, ny))
    
    return -1  # No path found

# Sample data - extracted from problem statement
samples = [
    ("""5,4
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
2,0""".strip().splitlines(), 22)
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
