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
    
    # BFS to find shortest path without cheating
    def bfs(start_pos, end_pos):
        from collections import deque
        queue = deque([(start_pos[0], start_pos[1], 0)])
        visited = set([start_pos])
        
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        while queue:
            r, c, dist = queue.popleft()
            
            if (r, c) == end_pos:
                return dist
            
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#' and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc, dist + 1))
        
        return float('inf')
    
    # Get shortest path distance without cheating
    shortest_path = bfs(start, end)
    
    # Precompute distances from start and to end for all track positions
    from collections import deque
    
    # Distances from start
    dist_from_start = {}
    queue = deque([(start[0], start[1], 0)])
    visited = set([start])
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while queue:
        r, c, dist = queue.popleft()
        dist_from_start[(r, c)] = dist
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#' and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc, dist + 1))
    
    # Distances to end
    dist_to_end = {}
    queue = deque([(end[0], end[1], 0)])
    visited = set([end])
    
    while queue:
        r, c, dist = queue.popleft()
        dist_to_end[(r, c)] = dist
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#' and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc, dist + 1))
    
    # Find all possible cheats
    cheats_count = 0
    
    # For each pair of track positions, check if using a cheat between them saves time
    track_positions = [pos for pos in dist_from_start.keys()]
    
    for i, (r1, c1) in enumerate(track_positions):
        for j, (r2, c2) in enumerate(track_positions):
            if i == j:
                continue
            
            # Manhattan distance between positions
            cheat_distance = abs(r1 - r2) + abs(c1 - c2)
            
            # If cheat distance is 2 or less (max 2 picoseconds cheat)
            if cheat_distance <= 2:
                # Calculate new path length: distance to cheat start + cheat distance + distance from cheat end to finish
                dist_to_start = dist_from_start[(r1, c1)]
                dist_from_end = dist_to_end[(r2, c2)]
                
                new_path_length = dist_to_start + cheat_distance + dist_from_end
                time_saved = shortest_path - new_path_length
                
                if time_saved >= 100:
                    cheats_count += 1
    
    return cheats_count

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

