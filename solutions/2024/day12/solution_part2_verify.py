import sys
from collections import deque

def solve_part2(lines):
    if not lines:
        return 0
    
    rows = len(lines)
    cols = len(lines[0])
    
    # Find all regions
    visited = [[False] * cols for _ in range(rows)]
    total_price = 0
    
    for r in range(rows):
        for c in range(cols):
            if not visited[r][c]:
                # Start BFS/DFS for this region
                plant_type = lines[r][c]
                queue = deque([(r, c)])
                visited[r][c] = True
                region_cells = []
                
                # Collect all cells in this region
                while queue:
                    curr_r, curr_c = queue.popleft()
                    region_cells.append((curr_r, curr_c))
                    
                    # Check neighbors
                    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and lines[nr][nc] == plant_type:
                            visited[nr][nc] = True
                            queue.append((nr, nc))
                
                # Calculate area and sides
                area = len(region_cells)
                sides = count_sides(lines, region_cells, plant_type)
                price = area * sides
                total_price += price
    
    return total_price

def count_sides(grid, region_cells, plant_type):
    """
    Count the number of sides for a region.
    A side is a continuous straight section of the boundary.
    """
    # Create a set for faster lookup
    region_set = set(region_cells)
    
    # Find all boundary edges (edges between region and non-region)
    # Each edge is represented as (cell_position, direction)
    boundary_edges = []
    
    for r, c in region_cells:
        # Check each of the 4 directions
        for dr, dc, direction in [(0, 1, 'right'), (1, 0, 'down'), (0, -1, 'left'), (-1, 0, 'up')]:
            nr, nc = r + dr, c + dc
            
            # If neighbor is outside grid or different plant type, this is a boundary edge
            if (nr < 0 or nr >= len(grid) or nc < 0 or nc >= len(grid[0]) or 
                grid[nr][nc] != plant_type):
                boundary_edges.append(((r, c), direction))
    
    if not boundary_edges:
        return 0
    
    # Group boundary edges by direction and position to find continuous sides
    sides = 0
    
    # For horizontal edges (left/right), group by row and check for continuity
    horizontal_edges = [((r, c), d) for (r, c), d in boundary_edges if d in ['left', 'right']]
    horizontal_edges.sort()
    
    # For vertical edges (up/down), group by column and check for continuity  
    vertical_edges = [((r, c), d) for (r, c), d in boundary_edges if d in ['up', 'down']]
    vertical_edges.sort()
    
    # Count horizontal sides
    sides += count_continuous_sides(horizontal_edges)
    
    # Count vertical sides
    sides += count_continuous_sides(vertical_edges)
    
    return sides

def count_continuous_sides(edges):
    """
    Count continuous sides from sorted edges.
    Two edges are continuous if they're adjacent in the same direction.
    """
    if not edges:
        return 0
    
    sides = 1  # Start with 1 for the first edge
    
    for i in range(1, len(edges)):
        prev_pos, prev_dir = edges[i-1]
        curr_pos, curr_dir = edges[i]
        
        # Check if edges are continuous
        if prev_dir == curr_dir:
            if prev_dir in ['left', 'right']:
                # Horizontal edges: continuous if same row and adjacent columns
                if prev_pos[0] == curr_pos[0] and prev_pos[1] + 1 == curr_pos[1]:
                    continue  # Part of same side
            else:
                # Vertical edges: continuous if same column and adjacent rows
                if prev_pos[1] == curr_pos[1] and prev_pos[0] + 1 == curr_pos[0]:
                    continue  # Part of same side
        
        # If not continuous, start a new side
        sides += 1
    
    return sides

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples.
samples = [
    ("AAAA\nBBCD\nBBCC\nEEEC", 80),
    ("OOOOO\nOXOXO\nOOOOO\nOXOXO\nOOOOO", 436),
    ("EEEEE\nEXXXX\nEEEEE\nEXXXX\nEEEEE", 236),
    ("AAAAAA\nAAABBA\nAAABBA\nABBAAA\nABBAAA\nAAAAAA", 368)
]

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part2(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 2: {sample_result} ----") # YOU MUST NOT change this output format

# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part2(lines)
print(f"---- FINAL result Part 2: {final_result} ----") # YOU MUST NOT change this output format
