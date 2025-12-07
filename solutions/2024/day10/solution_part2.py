from functools import lru_cache

def solve_part2(lines):
    # Parse the grid
    grid = []
    for line in lines:
        row = []
        for char in line:
            if char == '.':
                # Mark impassable cells with a special value (e.g., -1)
                row.append(-1)
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
    
    @lru_cache(maxsize=None)
    def count_paths(r, c, height):
        # If we reached height 9, this is a valid trail end
        if height == 9:
            return 1
        
        total = 0
        # Explore all 4 directions
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                next_height = grid[nr][nc]
                # Only move to next height (exactly +1)
                if next_height != -1 and next_height == height + 1:
                    total += count_paths(nr, nc, next_height)
        
        return total
    
    total_rating = 0
    for r, c in trailheads:
        total_rating += count_paths(r, c, 0)
    
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

