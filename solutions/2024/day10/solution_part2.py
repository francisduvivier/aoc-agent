from collections import deque

def solve_part2(lines):
    grid = []
    for line in lines:
        row = []
        for char in line:
            if char == '.':
                row.append(-1)  # Mark impassable tiles
            else:
                row.append(int(char))
        grid.append(row)
    
    rows, cols = len(grid), len(grid[0])
    
    # Find all trailheads (height 0)
    trailheads = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                trailheads.append((r, c))
    
    def count_trails(start_r, start_c):
        # Use DFS to count all distinct paths from start to any 9
        # We need to track visited positions per path to avoid cycles
        def dfs(r, c):
            if grid[r][c] == 9:
                return 1
            
            total = 0
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if grid[nr][nc] != -1 and grid[nr][nc] == grid[r][c] + 1:
                        total += dfs(nr, nc)
            return total
        
        return dfs(start_r, start_c)
    
    total_rating = 0
    for r, c in trailheads:
        total_rating += count_trails(r, c)
    
    return total_rating

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples.
samples = [
    (".....0.\n..4321.\n..5..2.\n..6543.\n..7..4.\n..8765.\n..9....", 3),
    ("..90..9\n...1.98\n...2..7\n6543456\n765.987\n876....\n987....", 227),
    ("89010123\n78121874\n87430965\n96549874\n45678903\n32019012\n01329801\n10456732", 81)
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
