def solve_part2(lines):
    grid = [list(line) for line in lines]
    h, w = len(grid), len(grid[0])
    visited = [[False] * w for _ in range(h)]
    
    def dfs(i, j, plant, region):
        if i < 0 or i >= h or j < 0 or j >= w or visited[i][j] or grid[i][j] != plant:
            return
        visited[i][j] = True
        region.add((i, j))
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            dfs(i + di, j + dj, plant, region)
    
    regions = []
    for i in range(h):
        for j in range(w):
            if not visited[i][j]:
                region = set()
                dfs(i, j, grid[i][j], region)
                regions.append(region)
    
    def count_sides(region):
        # Top sides
        top = set()
        for i, j in region:
            if i == 0 or (i - 1, j) not in region:
                top.add((i, j))
        top_sides = 0
        for i in range(h):
            row_top = sorted([j for ii, j in top if ii == i])
            if row_top:
                top_sides += 1
                for k in range(1, len(row_top)):
                    if row_top[k] != row_top[k - 1] + 1:
                        top_sides += 1
        
        # Bottom sides
        bottom = set()
        for i, j in region:
            if i == h - 1 or (i + 1, j) not in region:
                bottom.add((i, j))
        bottom_sides = 0
        for i in range(h):
            row_bottom = sorted([j for ii, j in bottom if ii == i])
            if row_bottom:
                bottom_sides += 1
                for k in range(1, len(row_bottom)):
                    if row_bottom[k] != row_bottom[k - 1] + 1:
                        bottom_sides += 1
        
        # Left sides
        left = set()
        for i, j in region:
            if j == 0 or (i, j - 1) not in region:
                left.add((i, j))
        left_sides = 0
        for j in range(w):
            col_left = sorted([i for i, jj in left if jj == j])
            if col_left:
                left_sides += 1
                for k in range(1, len(col_left)):
                    if col_left[k] != col_left[k - 1] + 1:
                        left_sides += 1
        
        # Right sides
        right = set()
        for i, j in region:
            if j == w - 1 or (i, j + 1) not in region:
                right.add((i, j))
        right_sides = 0
        for j in range(w):
            col_right = sorted([i for i, jj in right if jj == j])
            if col_right:
                right_sides += 1
                for k in range(1, len(col_right)):
                    if col_right[k] != col_right[k - 1] + 1:
                        right_sides += 1
        
        return top_sides + bottom_sides + left_sides + right_sides
    
    total = 0
    for region in regions:
        area = len(region)
        sides = count_sides(region)
        total += area * sides
    return total

# Sample data – populated with samples from the problem statement.
samples = [
    ("""AAAA
BBCD
BBCC
EEEC""", 80),
    ("""OOOOO
OXOXO
OOOOO
OXOXO
OOOOO""", 436),
]

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_res = solve_part2(sample_input.strip().splitlines())
    assert sample_res == expected_result, f"Sample {idx} result {sample_res} does not match expected {expected_result}"
    print(f"---- Sample {idx} Solution Part 2: {sample_res} ----")

# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part2(lines)
print(f"---- Final Solution Part 2: {final_result} ----")
