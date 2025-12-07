from collections import deque

def solve_part2(lines):
    if not lines or not lines[0]:
        return 0
    
    grid = [list(line.strip()) for line in lines]
    rows, cols = len(grid), len(grid[0])
    visited = set()
    total_price = 0
    
    for r in range(rows):
        for c in range(cols):
            if (r, c) in visited:
                continue
                
            plant_type = grid[r][c]
            queue = deque([(r, c)])
            region_cells = set([(r, c)])
            visited.add((r, c))
            
            while queue:
                cr, cc = queue.popleft()
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = cr + dr, cc + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == plant_type and (nr, nc) not in region_cells:
                        region_cells.add((nr, nc))
                        visited.add((nr, nc))
                        queue.append((nr, nc))
            
            sides = 0
            for cr, cc in region_cells:
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nr, nc = cr + dx, cc + dy
                    if not (0 <= nr < rows and 0 <= nc < cols) or grid[nr][nc] != plant_type:
                        sides += 1
            
            corners = 0
            for cr, cc in region_cells:
                for dx, dy in [(0.5, 0.5), (0.5, -0.5), (-0.5, 0.5), (-0.5, -0.5)]:
                    corner_r, corner_c = cr + dx, cc + dy
                    adjacent_cells = set()
                    for check_dx, check_dy in [(0.5, 0), (-0.5, 0), (0, 0.5), (0, -0.5)]:
                        check_r = corner_r + check_dx
                        check_c = corner_c + check_dy
                        if 0 <= check_r < rows and 0 <= check_c < cols:
                            adjacent_cells.add(grid[int(check_r)][int(check_c)])
                    
                    if len(adjacent_cells) == 1 and plant_type in adjacent_cells:
                        continue
                    corners += 1
            
            area = len(region_cells)
            total_price += area * (sides + corners)
    
    return total_price

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
    ("""EEEEE
EXXXX
EEEEE
EXXXX
EEEEE""", 236),
    ("""AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA""", 368),
    ("""RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE""", 1206)
]

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_res = solve_part2(sample_input.strip().splitlines())
    assert sample_res == expected_result, f"Sample {idx} result {sample_res} does not match expected {expected_result}"
    print(f"---- Sample {idx} Solution Part 2: {sample_res} ----")

with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part2(lines)
print(f"---- Final Solution Part 2: {final_result} ----")
