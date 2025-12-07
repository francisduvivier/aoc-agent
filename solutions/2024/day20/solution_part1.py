from collections import deque

def solve_part1(lines):
    # Find start and end positions
    start = end = None
    for r, row in enumerate(lines):
        for c, ch in enumerate(row):
            if ch == 'S':
                start = (r, c)
            elif ch == 'E':
                end = (r, c)
    
    # BFS to find shortest path distances from start and end
    def bfs_distances(start_pos):
        dist = {start_pos: 0}
        q = deque([start_pos])
        while q:
            r, c = q.popleft()
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < len(lines) and 0 <= nc < len(lines[0]) and lines[nr][nc] != '#' and (nr, nc) not in dist:
                    dist[(nr, nc)] = dist[(r, c)] + 1
                    q.append((nr, nc))
        return dist
    
    dist_from_start = bfs_distances(start)
    dist_from_end = bfs_distances(end)
    
    # Total shortest path distance
    total_dist = dist_from_start[end]
    
    # Count cheats that save at least 100 picoseconds
    count = 0
    for r1 in range(len(lines)):
        for c1 in range(len(lines[0])):
            if lines[r1][c1] == '#':
                continue
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                r2, c2 = r1 + dr, c1 + dc
                if 0 <= r2 < len(lines) and 0 <= c2 < len(lines[0]) and lines[r2][c2] != '#':
                    # Cheating path: start -> (r1,c1) -> (r2,c2) -> end
                    cheat_dist = dist_from_start[(r1, c1)] + 1 + dist_from_end[(r2, c2)]
                    saved = total_dist - cheat_dist
                    if saved >= 100:
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

