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
        # State: (r, c, height)
        queue = deque([(start_r, start_c, 0)])
        # visited[r][c] = set of heights that can reach this cell
        visited = [[set() for _ in range(cols)] for _ in range(rows)]
        visited[start_r][start_c].add(0)
        trail_count = 0
        
        while queue:
            r, c, height = queue.popleft()
            
            # If we reached height 9, count this as a completed trail
            if height == 9:
                trail_count += 1
                continue
            
            # Explore neighbors
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    next_height = grid[nr][nc]
                    # Must increase by exactly 1
                    if next_height == height + 1:
                        # Only add if we haven't visited this cell with this height before
                        if next_height not in visited[nr][nc]:
                            visited[nr][nc].add(next_height)
                            queue.append((nr, nc, next_height))
        
        return trail_count
    
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
