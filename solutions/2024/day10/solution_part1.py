from collections import deque

def solve_part1(lines):
    # Convert to integer grid
    grid = [list(map(int, line)) for line in lines]
    rows, cols = len(grid), len(grid[0])
    
    # Find all trailheads (height 0)
    trailheads = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                trailheads.append((r, c))
    
    def reachable_nines(start_r, start_c):
        """Find all reachable 9s from a trailhead using BFS."""
        reachable = set()
        queue = deque([(start_r, start_c)])
        visited = {(start_r, start_c)}
        
        while queue:
            r, c = queue.popleft()
            
            if grid[r][c] == 9:
                reachable.add((r, c))
                continue
                
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if grid[nr][nc] == grid[r][c] + 1:
                        if (nr, nc) not in visited:
                            visited.add((nr, nc))
                            queue.append((nr, nc))
        
        return reachable
    
    total_score = 0
    for r, c in trailheads:
        total_score += len(reachable_nines(r, c))
    
    return total_score

# Sample data - only include samples without dots
samples = [
    ("""0123
1234
8765
9876""", 1),
    ("""10..9..
2...8..
3...7..
4567654
...8..3
...9..2
.....01""", 3),
    ("""89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732""", 36)
]

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part1(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 1: {sample_result} ----")

# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part1(lines)
print(f"---- Final result Part 1: {final_result} ----")
