import sys
from collections import deque

def solve_part1(lines):
    # Parse grid
    grid = [list(line) for line in lines]
    R, C = len(grid), len(grid[0])
    
    # Find start and end
    start = end = None
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 'S':
                start = (r, c)
            elif grid[r][c] == 'E':
                end = (r, c)
    
    # BFS to get shortest distances from start and to end
    def bfs(src):
        dist = {src: 0}
        q = deque([src])
        while q:
            r, c = q.popleft()
            for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] != '#' and (nr, nc) not in dist:
                    dist[(nr, nc)] = dist[(r, c)] + 1
                    q.append((nr, nc))
        return dist
    
    dist_from_start = bfs(start)
    dist_to_end = bfs(end)
    
    # Cheats: exactly 2 steps through walls allowed
    # For each pair of track positions (u, v) with Manhattan distance <= 2,
    # if u and v are both track, the cheat saves:
    #   dist_from_start[u] + dist_to_end[v] + 2 - dist_from_start[v]
    # where dist_from_start[v] is the normal time.
    
    track_positions = [(r, c) for r in range(R) for c in range(C) if grid[r][c] != '#']
    
    count = 0
    seen_cheats = set()
    for u in track_positions:
        for v in track_positions:
            if u == v:
                continue
            # Manhattan distance must be <= 2
            if abs(u[0] - v[0]) + abs(u[1] - v[1]) > 2:
                continue
            # Cheats are uniquely identified by start and end positions
            # Start position is u, end position is v
            # Normal time: dist_from_start[v]
            # Cheated time: dist_from_start[u] + 2 + dist_to_end[v]
            normal = dist_from_start.get(v, float('inf'))
            cheated = dist_from_start.get(u, float('inf')) + 2 + dist_to_end.get(v, float('inf'))
            if normal != float('inf') and cheated != float('inf'):
                saved = normal - cheated
                if saved >= 100:
                    # Ensure unique cheats by start and end positions
                    cheat = (u, v)
                    if cheat not in seen_cheats:
                        seen_cheats.add(cheat)
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

