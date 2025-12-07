from collections import deque

def solve_part2(lines):
    # Parse the grid
    grid = [list(map(int, line)) for line in lines]
    rows, cols = len(grid), len(grid[0])
    
    # Find all trailheads (height 0)
    trailheads = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                trailheads.append((r, c))
    
    def count_trails(start_r, start_c):
        # BFS to find all distinct paths from start to any height 9
        # We need to count paths, not just reachable cells
        # State: (r, c, height)
        queue = deque([(start_r, start_c, 0)])
        # visited[r][c] = set of heights that can reach this cell
        # But we need to count paths, so we'll track path counts
        path_counts = {}
        path_counts[(start_r, start_c, 0)] = 1
        
        total_trails = 0
        
        while queue:
            r, c, height = queue.popleft()
            current_paths = path_counts.get((r, c, height), 0)
            
            # If we reached height 9, count all paths that reached this cell
            if height == 9:
                total_trails += current_paths
                continue
            
            # Explore neighbors
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    next_height = grid[nr][nc]
                    # Must increase by exactly 1
                    if next_height == height + 1:
                        next_state = (nr, nc, next_height)
                        # Add to queue if not already processed
                        if next_state not in path_counts:
                            queue.append(next_state)
                            path_counts[next_state] = 0
                        # Add the number of paths from current state to next state
                        path_counts[next_state] += current_paths
        
        return total_trails
    
    total_rating = 0
    for r, c in trailheads:
        total_rating += count_trails(r, c)
    
    return total_rating

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples.
samples = [
    ("""89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732""", 81),
    (""".....0.
..4321.
..5..2.
..6543.
..7..4.
..8765.
..9....""", 3),
    ("""..90..9
...1.98
...2..7
6543456
765.987
876....
987....""", 227)
]  # TODO: fill with actual samples and expected results

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part2(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 2: {sample_result} ----") # YOU MUST NOT change this output format

# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part2(lines)
print(f"---- Final result Part 2: {final_result} ----") # YOU MUST NOT change this output format

