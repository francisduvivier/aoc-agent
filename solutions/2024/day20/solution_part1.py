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
    
    # BFS to find shortest path from start to end
    def bfs(start_pos, end_pos):
        queue = deque([(start_pos, 0)])
        visited = {start_pos}
        while queue:
            (r, c), dist = queue.popleft()
            if (r, c) == end_pos:
                return dist
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < len(lines) and 0 <= nc < len(lines[0]) and lines[nr][nc] != '#' and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append(((nr, nc), dist + 1))
        return float('inf')
    
    # Get shortest path distance without cheating
    shortest_path = bfs(start, end)
    
    # Precompute distances from start to all positions
    start_distances = {}
    queue = deque([(start, 0)])
    visited = {start}
    while queue:
        (r, c), dist = queue.popleft()
        start_distances[(r, c)] = dist
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(lines) and 0 <= nc < len(lines[0]) and lines[nr][nc] != '#' and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append(((nr, nc), dist + 1))
    
    # Precompute distances from all positions to end
    end_distances = {}
    queue = deque([(end, 0)])
    visited = {end}
    while queue:
        (r, c), dist = queue.popleft()
        end_distances[(r, c)] = dist
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(lines) and 0 <= nc < len(lines[0]) and lines[nr][nc] != '#' and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append(((nr, nc), dist + 1))
    
    # Find all track positions
    track_positions = []
    for r in range(len(lines)):
        for c in range(len(lines[0])):
            if lines[r][c] != '#':
                track_positions.append((r, c))
    
    # For each pair of positions with Manhattan distance <= 2
    count = 0
    for i in range(len(track_positions)):
        for j in range(i + 1, len(track_positions)):
            r1, c1 = track_positions[i]
            r2, c2 = track_positions[j]
            
            # Manhattan distance must be <= 2 for a valid cheat
            manhattan_dist = abs(r1 - r2) + abs(c1 - c2)
            if manhattan_dist > 2:
                continue
            
            # Check if both positions are reachable
            if (r1, c1) not in start_distances or (r2, c2) not in end_distances:
                continue
            
            # Calculate path distances
            dist_start_to_cheat_start = start_distances[(r1, c1)]
            dist_cheat_end_to_end = end_distances[(r2, c2)]
            
            # Total distance with cheat
            total_with_cheat = dist_start_to_cheat_start + manhattan_dist + dist_cheat_end_to_end
            
            # Time saved
            time_saved = shortest_path - total_with_cheat
            
            if time_saved >= 100:
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
