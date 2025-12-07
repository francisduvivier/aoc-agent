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
            
            # Count sides by tracing boundaries
            sides = 0
            # For each cell, check corners to count sides
            for r, c in region_cells:
                # Check all 8 neighbors for boundary detection
                # A side exists at a corner if the diagonal is not part of the region
                # but at least one adjacent orthogonal cell is also not part of the region
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        # If neighbor is out of bounds or different type
                        if not (0 <= nr < rows and 0 <= nc < cols) or grid[nr][nc] != plant_type:
                            # Check if this creates a new side (corner case)
                            # For orthogonal neighbors, always count as side
                            if abs(dr) + abs(dc) == 1:
                                sides += 1
                            # For diagonal neighbors, count if both adjacent orthogonals are not in region
                            else:
                                orth1_ok = (0 <= r + dr < rows and 0 <= c < cols and grid[r + dr][c] == plant_type)
                                orth2_ok = (0 <= r < rows and 0 <= c + dc < cols and grid[r][c + dc] == plant_type)
                                if not orth1_ok and not orth2_ok:
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
