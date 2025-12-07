from collections import defaultdict

def solve_part2(lines):
    grid = [list(line) for line in lines if line.strip()]
    if not grid:
        return 0
    rows = len(grid)
    cols = len(grid[0])
    visited = set()
    regions = []
    
    # Find all regions using BFS
    for i in range(rows):
        for j in range(cols):
            if (i, j) not in visited:
                plant = grid[i][j]
                region = set()
                queue = [(i, j)]
                visited.add((i, j))
                region.add((i, j))
                while queue:
                    x, y = queue.pop(0)
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == plant and (nx, ny) not in visited:
                            visited.add((nx, ny))
                            region.add((nx, ny))
                            queue.append((nx, ny))
                regions.append(region)
    
    total_price = 0
    for region in regions:
        area = len(region)
        sides = 0
        
        # Collect fence positions for each direction
        top_fences = []
        bottom_fences = []
        left_fences = []
        right_fences = []
        for i, j in region:
            if i - 1 < 0 or (i - 1, j) not in region:
                top_fences.append((i, j))
            if i + 1 >= rows or (i + 1, j) not in region:
                bottom_fences.append((i, j))
            if j - 1 < 0 or (i, j - 1) not in region:
                left_fences.append((i, j))
            if j + 1 >= cols or (i, j + 1) not in region:
                right_fences.append((i, j))
        
        # Count sides for top and bottom (horizontal)
        for fences, is_top in [(top_fences, True), (bottom_fences, False)]:
            row_groups = defaultdict(list)
            for i, j in fences:
                row_groups[i].append(j)
            for i, js in row_groups.items():
                js.sort()
                count = 1
                for k in range(1, len(js)):
                    if js[k] > js[k-1] + 1:
                        count += 1
                sides += count
        
        # Count sides for left and right (vertical)
        for fences, is_left in [(left_fences, True), (right_fences, False)]:
            col_groups = defaultdict(list)
            for i, j in fences:
                col_groups[j].append(i)
            for j, is_ in col_groups.items():
                is_.sort()
                count = 1
                for k in range(1, len(is_)):
                    if is_[k] > is_[k-1] + 1:
                        count += 1
                sides += count
        
        price = area * sides
        total_price += price
    
    return total_price

# Sample data – extracted from the problem statement
samples = [
    ("AAAA\nBBCD\nBBCC\nEEEC", 80),
    ("OOOOO\nOXOXO\nOOOOO\nOXOXO\nOOOOO", 436),
    ("EEEEE\nEXXXX\nEEEEE\nEXXXX\nEEEEE", 236),
    ("AAAAAA\nAAABBA\nAAABBA\nABBAAA\nABBAAA\nAAAAAA", 368),
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
