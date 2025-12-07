```python
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
    
    # Find all possible cheat shortcuts
    cheats_saved = []
    
    # Get all track positions
    track_positions = []
    for r, row in enumerate(lines):
        for c, ch in enumerate(row):
            if ch in '.SE':
                track_positions.append((r, c))
    
    # For each pair of track positions, check if they can be connected with a cheat
    for i, pos1 in enumerate(track_positions):
        for pos2 in track_positions[i+1:]:
            r1, c1 = pos1
            r2, c2 = pos2
            
            # Check if positions are exactly 2 steps apart (Manhattan distance = 2)
            if abs(r1 - r2) + abs(c1 - c2) != 2:
                continue
            
            # BFS from start to pos1, then cheat to pos2, then BFS to end
            dist_to_pos1 = bfs(start, pos1)
            if dist_to_pos1 == float('inf'):
                continue
                
            dist_from_pos2 = bfs(pos2, end)
            if dist_from_pos2 == float('inf'):
                continue
            
            # Total distance with cheat
            total_with_cheat = dist_to_pos1 + 1 + dist_from_pos2
            
            # Time saved
            time_saved = shortest_path - total_with_cheat
            
            if time_saved >= 100:
                cheats_saved.append(time_saved)
    
    return len(cheats_saved)

# Sample data - may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples.
samples = []  # TODO: fill with actual samples and expected results

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part1(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx}