import sys
from collections import deque

def solve_part1(lines):
    # Parse grid and find start/end
    grid = [list(line) for line in lines]
    R, C = len(grid), len(grid[0])
    
    start = end = None
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 'S':
                start = (r, c)
            elif grid[r][c] == 'E':
                end = (r, c)
    
    # BFS to get shortest path distances from start and to end
    def bfs_dist(source):
        dist = [[-1] * C for _ in range(R)]
        q = deque([source])
        dist[source[0]][source[1]] = 0
        while q:
            r, c = q.popleft()
            for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] != '#' and dist[nr][nc] == -1:
                    dist[nr][nc] = dist[r][c] + 1
                    q.append((nr, nc))
        return dist
    
    dist_from_start = bfs_dist(start)
    dist_to_end = bfs_dist(end)
    
    # Cheats: exactly 2 steps through walls, start and end on track
    # Enumerate all pairs of positions at Manhattan distance <= 2
    # Count cheats saving >= 100 picoseconds
    threshold = 100
    count = 0
    
    for r1 in range(R):
        for c1 in range(C):
            if grid[r1][c1] == '#': continue
            if dist_from_start[r1][c1] == -1: continue
            
            for r2 in range(R):
                for c2 in range(C):
                    if grid[r2][c2] == '#': continue
                    if dist_to_end[r2][c2] == -1: continue
                    
                    # Manhattan distance must be <= 2 (cheat length)
                    md = abs(r1 - r2) + abs(c1 - c2)
                    if md == 0 or md > 2: continue
                    
                    # Original path length via normal track
                    original = dist_from_start[r1][c1] + dist_to_end[r2][c2]
                    # Cheated path length
                    cheated = dist_from_start[r1][c1] + md + dist_to_end[r2][c2]
                    saved = original - cheated
                    if saved >= threshold:
                        count += 1
                        
    return count

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
