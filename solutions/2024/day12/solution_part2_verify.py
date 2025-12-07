import sys
from collections import deque

# Sample inputs and expected results for part 2
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
    region_cells = set()
    queue = deque([(start_r, start_c)])
    region_cells.add((start_r, start_c))
    visited.add((start_r, start_c))
    
    while queue:
        r, c = queue.popleft()
        for nr, nc in get_neighbors(r, c, len(grid), len(grid[0])):
            if (nr, nc) not in visited and grid[nr][nc] == plant_type:
                visited.add((nr, nc))
                region_cells.add((nr, nc))
                queue.append((nr, nc))
    
    return region_cells

def get_perimeter_sides(grid, region_cells):
    # Collect all exposed edges with their orientations
    # Represent edges as (position, orientation) where:
    # - For horizontal edges: (row, col_start, 'H')
    # - For vertical edges: (row_start, col, 'V')
    
    horizontal_edges = []
    vertical_edges = []
    
    for r, c in region_cells:
        # Top edge: between (r-1,c) and (r,c)
        if r == 0 or (r-1, c) not in region_cells:
            horizontal_edges.append((r, c, 'H'))
        # Bottom edge: between (r,c) and (r+1,c)
        if r == len(grid) - 1 or (r+1, c) not in region_cells:
            horizontal_edges.append((r+1, c, 'H'))
        # Left edge: between (r,c-1) and (r,c)
        if c == 0 or (r, c-1) not in region_cells:
            vertical_edges.append((r, c, 'V'))
        # Right edge: between (r,c) and (r,c+1)
        if c == len(grid[0]) - 1 or (r, c+1) not in region_cells:
            vertical_edges.append((r, c+1, 'V'))
    
    # Count continuous segments
    horizontal_sides = count_continuous_segments(horizontal_edges, is_horizontal=True)
    vertical_sides = count_continuous_segments(vertical_edges, is_horizontal=False)
    
    return horizontal_sides + vertical_sides

def count_continuous_segments(edges, is_horizontal):
    if not edges:
        return 0
    
    # Group edges by their fixed coordinate
    if is_horizontal:
        # Group by row (first coordinate)
        edges_by_coord = {}
        for r, c, _ in edges:
            if r not in edges_by_coord:
                edges_by_coord[r] = []
            edges_by_coord[r].append(c)
    else:
        # Group by column (second coordinate)
        edges_by_coord = {}
        for r, c, _ in edges:
            if c not in edges_by_coord:
                edges_by_coord[c] = []
            edges_by_coord[c].append(r)
    
    segments = 0
    for coord, positions in edges_by_coord.items():
        positions.sort()
        # Count continuous segments
        if positions:
            segments += 1
            for i in range(1, len(positions)):
                if positions[i] != positions[i-1] + 1:
                    segments += 1
    
    return segments

def solve_part2(grid):
    rows, cols = len(grid), len(grid[0])
    visited = set()
    total_price = 0
    
    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                region_cells = flood_fill(grid, r, c, visited)
                area = len(region_cells)
                sides = get_perimeter_sides(grid, region_cells)
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
    
    # Solve for actual input
    try:
        with open('input.txt', 'r') as f:
            input_text = f.read()
        
        grid = parse_input(input_text)
        result = solve_part2(grid)
        print(f"---- Actual Input Solution Part 2: {result} ----")
        
    except FileNotFoundError:
        print("input.txt not found, skipping actual input")
    except Exception as e:
        print(f"Error reading input.txt: {e}")

if __name__ == "__main__":
    main()
