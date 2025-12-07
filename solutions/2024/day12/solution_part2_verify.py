import sys
from collections import deque

# Sample inputs and expected results
samples = [
    ("AAAA\nBBCD\nBBCC\nEEEC", 80),
    ("OOOOO\nOXOXO\nOOOOO\nOXOXO\nOOOOO", 436),
    ("EEEEE\nEXXXX\nEEEEE\nEXXXX\nEEEEE", 236),
    ("AAAAAA\nAAABBA\nAAABBA\nABBAAA\nABBAAA\nAAAAAA", 368),
    ("RRRRIICCFF\nRRRRIICCCF\nVVRRRCCFFF\nVVRCCCJFFF\nVVVVCJJCFE\nVVIVCCJJEE\nVVIIICJJEE\nMIIIIIJJEE\nMIIISIJEEE\nMMMISSJEEE", 1206)
]

def parse_input(text):
    return [list(line) for line in text.strip().split('\n')]

def get_neighbors(r, c, rows, cols):
    neighbors = []
    if r > 0:
        neighbors.append((r-1, c))
    if r < rows - 1:
        neighbors.append((r+1, c))
    if c > 0:
        neighbors.append((r, c-1))
    if c < cols - 1:
        neighbors.append((r, c+1))
    return neighbors

def flood_fill(grid, start_r, start_c, visited):
    plant_type = grid[start_r][start_c]
    rows, cols = len(grid), len(grid[0])
    
    # BFS to find all cells in this region
    queue = deque([(start_r, start_c)])
    visited.add((start_r, start_c))
    region_cells = [(start_r, start_c)]
    
    while queue:
        r, c = queue.popleft()
        for nr, nc in get_neighbors(r, c, rows, cols):
            if (nr, nc) not in visited and grid[nr][nc] == plant_type:
                visited.add((nr, nc))
                queue.append((nr, nc))
                region_cells.append((nr, nc))
    
    return region_cells

def count_sides(grid, region_cells):
    # For each cell in the region, check each of its 4 edges
    # An edge is part of the perimeter if it's on the boundary of the grid
    # or if the adjacent cell in that direction is outside the region
    
    # Represent edges as (r, c, direction) where direction is 0=up, 1=right, 2=down, 3=left
    perimeter_edges = set()
    
    for r, c in region_cells:
        # Check up edge
        if r == 0 or (r-1, c) not in region_cells:
            perimeter_edges.add((r, c, 0))
        
        # Check right edge
        if c == len(grid[0]) - 1 or (r, c+1) not in region_cells:
            perimeter_edges.add((r, c, 1))
        
        # Check down edge
        if r == len(grid) - 1 or (r+1, c) not in region_cells:
            perimeter_edges.add((r, c, 2))
        
        # Check left edge
        if c == 0 or (r, c-1) not in region_cells:
            perimeter_edges.add((r, c, 3))
    
    # Now group edges into continuous straight segments (sides)
    sides = 0
    
    while perimeter_edges:
        # Start a new side with any edge
        start_edge = perimeter_edges.pop()
        r, c, direction = start_edge
        
        # Add this edge to the current side
        current_side = {start_edge}
        
        # Try to extend the side in both directions along the same line
        # For horizontal edges (up/down), we extend left/right
        # For vertical edges (left/right), we extend up/down
        
        if direction in [0, 2]:  # Up or down edge - horizontal line
            # Extend left
            cr, cc = r, c
            while True:
                if direction == 0:  # up edge
                    next_edge = (cr, cc-1, 0)
                else:  # down edge
                    next_edge = (cr, cc-1, 2)
                
                if next_edge in perimeter_edges:
                    perimeter_edges.remove(next_edge)
                    current_side.add(next_edge)
                    cc -= 1
                else:
                    break
            
            # Extend right
            cr, cc = r, c
            while True:
                if direction == 0:  # up edge
                    next_edge = (cr, cc+1, 0)
                else:  # down edge
                    next_edge = (cr, cc+1, 2)
                
                if next_edge in perimeter_edges:
                    perimeter_edges.remove(next_edge)
                    current_side.add(next_edge)
                    cc += 1
                else:
                    break
        
        else:  # Left or right edge - vertical line
            # Extend up
            cr, cc = r, c
            while True:
                if direction == 1:  # right edge
                    next_edge = (cr-1, cc, 1)
                else:  # left edge
                    next_edge = (cr-1, cc, 3)
                
                if next_edge in perimeter_edges:
                    perimeter_edges.remove(next_edge)
                    current_side.add(next_edge)
                    cr -= 1
                else:
                    break
            
            # Extend down
            cr, cc = r, c
            while True:
                if direction == 1:  # right edge
                    next_edge = (cr+1, cc, 1)
                else:  # left edge
                    next_edge = (cr+1, cc, 3)
                
                if next_edge in perimeter_edges:
                    perimeter_edges.remove(next_edge)
                    current_side.add(next_edge)
                    cr += 1
                else:
                    break
        
        sides += 1
    
    return sides

def solve_part2(grid):
    rows, cols = len(grid), len(grid[0])
    visited = set()
    total_price = 0
    
    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                region_cells = set(flood_fill(grid, r, c, visited))
                area = len(region_cells)
                sides = count_sides(grid, region_cells)
                price = area * sides
                total_price += price
    
    return total_price

def main():
    # Test samples
    for i, (sample_input, expected) in enumerate(samples):
        grid = parse_input(sample_input)
        result = solve_part2(grid)
        print(f"---- Sample {i+1} Solution Part 2: {result} ----")
        assert result == expected, f"Sample {i+1} failed: expected {expected}, got {result}"
    
    # Solve for input.txt
    try:
        with open('input.txt', 'r') as f:
            input_text = f.read()
        
        grid = parse_input(input_text)
        result = solve_part2(grid)
        print(f"---- Input Solution Part 2: {result} ----")
        
    except FileNotFoundError:
        print("input.txt not found, skipping main input")

if __name__ == "__main__":
    main()
