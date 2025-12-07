import heapq

def solve_part1(lines):
    # Parse byte positions
    bytes = []
    for line in lines:
        x, y = map(int, line.split(','))
        bytes.append((x, y))
    
    # Simulate first 1024 bytes falling
    grid_size = 70
    corrupted = set(bytes[:1024])
    
    # BFS to find shortest path
    start = (0, 0)
    end = (grid_size, grid_size)
    
    # Priority queue for Dijkstra's algorithm (all edges have weight 1)
    pq = [(0, start)]
    visited = {start: 0}
    
    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while pq:
        dist, current = heapq.heappop(pq)
        
        if current == end:
            return dist
            
        if dist > visited.get(current, float('inf')):
            continue
            
        x, y = current
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            # Check bounds
            if 0 <= nx <= grid_size and 0 <= ny <= grid_size:
                if (nx, ny) not in corrupted:
                    new_dist = dist + 1
                    
                    if (nx, ny) not in visited or new_dist < visited[(nx, ny)]:
                        visited[(nx, ny)] = new_dist
                        heapq.heappush(pq, (new_dist, (nx, ny)))
    
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
2,0""", 22)
]

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part1(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 1: {sample_result} ----")

# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part1(lines)
print(f"---- Final result Part 1: {final_result} ----")
