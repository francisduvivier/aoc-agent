from collections import deque

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
    
    # BFS to find shortest path distances from start and to end
    def bfs_distances(source):
        dist = [[-1] * cols for _ in range(rows)]
        dist[source[0]][source[1]] = 0
        queue = deque([source])
        while queue:
            r, c = queue.popleft()
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#' and dist[nr][nc] == -1:
                    dist[nr][nc] = dist[r][c] + 1
                    queue.append((nr, nc))
        return dist
    
    dist_from_start = bfs_distances(start)
    dist_to_end = bfs_distances(end)
    
    # Total shortest path distance from start to end
    total_distance = dist_from_start[end[0]][end[1]]
    
    # Count cheats that save at least 100 picoseconds
    count = 0
    for r1 in range(rows):
        for c1 in range(cols):
            if grid[r1][c1] == '#':
                continue
            for r2 in range(rows):
                for c2 in range(cols):
                    if grid[r2][c2] == '#':
                        continue
                    # Manhattan distance between cheat start and end
                    cheat_distance = abs(r1 - r2) + abs(c2 - c1)
                    if cheat_distance <= 2:  # Valid cheat (up to 2 picoseconds)
                        # Original distance from start to r1 to r2 to end
                        original = dist_from_start[r1][c1] + dist_to_end[r2][c2]
                        # New distance with cheat
                        new_dist = dist_from_start[r1][c1] + cheat_distance + dist_to_end[r2][c2]
                        # Time saved
                        saved = original - new_dist
                        if saved >= 100:
                            count += 1
    return count

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
