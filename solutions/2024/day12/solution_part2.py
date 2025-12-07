from collections import deque

def solve_part2(lines):
    grid = [list(line) for line in lines]
    rows, cols = len(grid), len(grid[0])
    visited = set()
    total_price = 0
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    for r in range(rows):
        for c in range(cols):
            if (r, c) in visited:
                continue
                
            plant_type = grid[r][c]
            queue = deque([(r, c)])
            visited.add((r, c))
            region_cells = set([(r, c)])
            
            while queue:
                cr, cc = queue.popleft()
                for dr, dc in directions:
                    nr, nc = cr + dr, cc + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == plant_type and (nr, nc) not in visited:
                        visited.add((nr, nc))
                        region_cells.add((nr, nc))
                        queue.append((nr, nc))
            
            sides = 0
            for cell in region_cells:
                r, c = cell
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if not (0 <= nr < rows and 0 <= nc < cols) or grid[nr][nc] != plant_type:
                        sides += 1
            
            area = len(region_cells)
            total_price += area * sides
    
    return total_price

sample_input = """AAAA
BBCD
BBCC
EEEC"""

expected_sample_result = 80

sample_result = solve_part2(sample_input.strip().splitlines())
assert sample_result == expected_sample_result, f"Sample result {sample_result} does not match expected {expected_sample_result}"
print(f"---- Sample Solution Part 2: {sample_result} ----")

with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part2(lines)
print(f"---- Final Solution Part 2: {final_result} ----")
