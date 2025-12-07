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
            
            corners = set()
            for cr, cc in region_cells:
                corners.add((cr, cc))
                corners.add((cr, cc + 1))
                corners.add((cr + 1, cc))
                corners.add((cr + 1, cc + 1))
            
            connected_corners = set()
            corner_components = []
            
            for corner in corners:
                if corner in connected_corners:
                    continue
                    
                queue = deque([corner])
                component = set([corner])
                connected_corners.add(corner)
                
                while queue:
                    cx, cy = queue.popleft()
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = cx + dx, cy + dy
                        if (nx, ny) in corners and (nx, ny) not in component:
                            component.add((nx, ny))
                            connected_corners.add((nx, ny))
                            queue.append((nx, ny))
                
                corner_components.append(component)
            
            sides = len(corner_components)
            area = len(region_cells)
            total_price += area * sides
    
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
