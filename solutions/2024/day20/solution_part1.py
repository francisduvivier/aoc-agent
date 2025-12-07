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
    
    # BFS to get distances from start and to end
    def bfs(src, target=None):
        dist = {src: 0}
        q = deque([src])
        while q:
            r, c = q.popleft()
            if target is not None and (r, c) == target:
                return dist[target]
            for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] != '#' and (nr, nc) not in dist:
                    dist[(nr, nc)] = dist[(r, c)] + 1
                    q.append((nr, nc))
        return dist
    
    dist_from_start = bfs(start)
    dist_to_end = bfs(end)
    
    # Cheats: exactly 2 steps through walls allowed
    # For each pair of points (u, v) with Manhattan distance <= 2,
    # if u and v are both track and reachable,
    # cheat time = dist_from_start[u] + 1 + (1 if dist(u,v)==2 else 0) + dist_to_end[v]
    # Actually simpler: cheat saves (dist_from_start[u] + dist_to_end[v] + cheat_len) - (dist_from_start[v] + dist_to_end[v])
    # But since we want savings >= 100, we can compute savings directly.
    
    savings_threshold = 100
    cheats = 0
    
    # All track positions
    track = [(r, c) for r in range(R) for c in range(C) if grid[r][c] != '#']
    
    # For each track position u as cheat start
    for r1, c1 in track:
        if (r1, c1) not in dist_from_start:
            continue
        # For each track position v as cheat end within Manhattan distance 2
        for r2, c2 in track:
            if (r2, c2) not in dist_to_end:
                continue
            # Manhattan distance
            md = abs(r1 - r2) + abs(c1 - c2)
            if md == 0 or md > 2:
                continue
            # Cheats are uniquely identified by start and end positions
            # Normal time from u to v along track
            normal_time = dist_from_start.get((r2, c2), float('inf')) - dist_from_start[(r1, c1)]
            if normal_time < 0:
                continue
            # Cheat time: md steps (through walls)
            cheat_time = md
            # Savings
            savings = normal_time - cheat_time
            if savings >= savings_threshold:
                cheats += 1
                
    return cheats

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
