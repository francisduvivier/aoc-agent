from collections import deque

def solve_part2(lines):
    grid = [list(line) for line in lines]
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
                queue = deque([(i, j)])
                visited.add((i, j))
                region.add((i, j))
                while queue:
                    x, y = queue.popleft()
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
        
        # Horizontal fences
        for i in range(rows):
            # Top fences
            top_fences = [j for j in range(cols) if (i, j) in region and (i - 1 < 0 or (i - 1, j) not in region)]
            if top_fences:
                sides += 1
                for k in range(1, len(top_fences)):
                    if top_fences[k] != top_fences[k-1] + 1:
                        sides += 1
            # Bottom fences
            bottom_fences = [j for j in range(cols) if (i, j) in region and (i + 1 >= rows or (i + 1, j) not in region)]
            if bottom_fences:
                sides += 1
                for k in range(1, len(bottom_fences)):
                    if bottom_fences[k] != bottom_fences[k-1] + 1:
                        sides += 1
        
        # Vertical fences
        for j in range(cols):
            # Left fences
            left_fences = [i for i in range(rows) if (i, j) in region and (j - 1 < 0 or (i, j - 1) not in region)]
            if left_fences:
                sides += 1
                for k in range(1, len(left_fences)):
                    if left_fences[k] != left_fences[k-1] + 1:
                        sides += 1
            # Right fences
            right_fences = [i for i in range(rows) if (i, j) in region and (j + 1 >= cols or (i, j + 1) not in region)]
            if right_fences:
                sides += 1
                for k in range(1, len(right_fences)):
                    if right_fences[k] != right_fences[k-1] + 1:
                        sides += 1
        
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
