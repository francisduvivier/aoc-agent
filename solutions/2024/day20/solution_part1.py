# Edit this file: implement solve_part1

def solve_part1(lines):
    # Parse the grid
    grid = [list(line) for line in lines]
    rows, cols = len(grid), len(grid[0])

    # Find start and end positions
    start = end = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'S':
                start = (r, c)
            elif grid[r][c] == 'E':
                end = (r, c)

    # BFS to find shortest path distances from start
    def bfs_distances(start_pos):
        from collections import deque
        dist = {start_pos: 0}
        q = deque([start_pos])
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        while q:
            r, c = q.popleft()
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#' and (nr, nc) not in dist:
                    dist[(nr, nc)] = dist[(r, c)] + 1
                    q.append((nr, nc))
        return dist

    # Get distances from start and to end
    dist_from_start = bfs_distances(start)
    dist_to_end = bfs_distances(end)
    
    # Total shortest path distance
    total_dist = dist_from_start.get(end, float('inf'))
    
    # Count cheats that save at least 100 picoseconds
    count = 0
    threshold = 100
    
    # Check all pairs of positions within Manhattan distance <= 20 (cheat distance)
    for pos1 in dist_from_start:
        r1, c1 = pos1
        for dr in range(-20, 21):
            for dc in range(-20, 21):
                if abs(dr) + abs(dc) > 20:  # Manhattan distance limit
                    continue
                r2, c2 = r1 + dr, c1 + dc
                pos2 = (r2, c2)
                
                if not (0 <= r2 < rows and 0 <= c2 < cols):
                    continue
                if pos1 == pos2:
                    continue
                
                # Calculate cheat distance (Manhattan distance)
                cheat_dist = abs(dr) + abs(dc)
                if cheat_dist > 20:  # Cheat limit
                    continue
                
                # Check if both positions are on the shortest path
                if pos1 not in dist_from_start or pos2 not in dist_to_end:
                    continue
                
                # Calculate new path length with cheat
                new_dist = dist_from_start[pos1] + cheat_dist + dist_to_end[pos2]
                
                # Calculate time saved
                saved = total_dist - new_dist
                
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
