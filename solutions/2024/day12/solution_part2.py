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
            
            # BFS to find all connected cells of same type
            while queue:
                cr, cc = queue.popleft()
                for dr, dc in directions:
                    nr, nc = cr + dr, cc + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == plant_type and (nr, nc) not in visited:
                        visited.add((nr, nc))
                        region_cells.add((nr, nc))
                        queue.append((nr, nc))
            
            # Count sides by checking adjacent cells
            sides = 0
            for cr, cc in region_cells:
                # Check all four directions
                for dr, dc in directions:
                    nr, nc = cr + dr, cc + dc
                    # If neighbor is out of bounds or different type, it's a side
                    if not (0 <= nr < rows and 0 <= nc < cols) or grid[nr][nc] != plant_type:
                        sides += 1
                    # Check diagonal connections that create corners
                    # For each corner, check if both adjacent sides exist
                    if dr == 0:  # horizontal movement
                        # Check above and below the horizontal neighbor
                        for vd in [1, -1]:
                            vr, vc = cr + vd, cc + dc
                            if (0 <= vr < rows and 0 <= vc < cols and 
                                grid[vr][vc] == plant_type and 
                                (vr, vc) not in region_cells):
                                sides += 1
                    else:  # vertical movement
                        # Check left and right of the vertical neighbor
                        for hd in [1, -1]:
                            hr, hc = cr + dr, cc + hd
                            if (0 <= hr < rows and 0 <= hc < cols and 
                                grid[hr][hc] == plant_type and 
                                (hr, hc) not in region_cells):
                                sides += 1
            
            area = len(region_cells)
            total_price += area * sides
    
    return total_price

# Sample data from the problem statement
sample_input = """AAAA
BBCD
BBCC
EEEC"""

expected_sample_result = 80

# Run on the sample and verify
sample_result = solve_part2(sample_input.strip().splitlines())
assert sample_result == expected_sample_result, f"Sample result {sample_result} does not match expected {expected_sample_result}"
print(f"---- Sample Solution Part 2: {sample_result} ----")

# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part2(lines)
print(f"---- Final Solution Part 2: {final_result} ----")
