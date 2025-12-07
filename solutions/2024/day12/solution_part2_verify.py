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

def count_sides(grid, region_cells):
    # For each cell in the region, find its sides
    # A side is a contiguous segment of edges that face the same direction
    # We'll collect all edges and then group them by direction and alignment
    
    edges = set()
    for r, c in region_cells:
        # Add edges for each side of the cell
        # Top edge: (r, c, 'T')
        # Right edge: (r, c, 'R')
        # Bottom edge: (r, c, 'B')
        # Left edge: (r, c, 'L')
        edges.add((r, c, 'T'))
        edges.add((r, c, 'R'))
        edges.add((r, c, 'B'))
        edges.add((r, c, 'L'))
    
    # Remove edges that are internal to the region
    internal_edges = set()
    for r, c in region_cells:
        # Check if neighbor in each direction is also in the region
        if (r-1, c) in region_cells:
            # Remove top edge of current cell and bottom edge of cell above
            internal_edges.add((r, c, 'T'))
            internal_edges.add((r-1, c, 'B'))
        if (r+1, c) in region_cells:
            internal_edges.add((r, c, 'B'))
            internal_edges.add((r+1, c, 'T'))
        if (r, c-1) in region_cells:
            internal_edges.add((r, c, 'L'))
            internal_edges.add((r, c-1, 'R'))
        if (r, c+1) in region_cells:
            internal_edges.add((r, c, 'R'))
            internal_edges.add((r, c+1, 'L'))
    
    # Remaining edges are the perimeter edges
    perimeter_edges = edges - internal_edges
    
    # Group edges by direction and alignment to count sides
    sides = 0
    
    # Group by direction
    for direction in ['T', 'R', 'B', 'L']:
        dir_edges = [edge for edge in perimeter_edges if edge[2] == direction]
        
        if direction in ['T', 'B']:
            # For top/bottom edges, group by row and contiguous columns
            # Sort by column
            dir_edges.sort(key=lambda x: (x[0], x[1]))
            i = 0
            while i < len(dir_edges):
                r = dir_edges[i][0]
                c = dir_edges[i][1]
                # Find contiguous segment
                j = i
                while j < len(dir_edges) and dir_edges[j][0] == r and dir_edges[j][1] == c + (j - i):
                    j += 1
                # Found a contiguous segment
                sides += 1
                i = j
        else:
            # For left/right edges, group by column and contiguous rows
            # Sort by row
            dir_edges.sort(key=lambda x: (x[1], x[0]))
            i = 0
            while i < len(dir_edges):
                c = dir_edges[i][1]
                r = dir_edges[i][0]
                # Find contiguous segment
                j = i
                while j < len(dir_edges) and dir_edges[j][1] == c and dir_edges[j][0] == r + (j - i):
                    j += 1
                # Found a contiguous segment
                sides += 1
                i = j
    
    return sides

def solve_part2(grid):
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    total_price = 0
    
    for r in range(rows):
        for c in range(cols):
            if not visited[r][c]:
                # Start BFS/DFS to find all connected cells of the same type
                plant_type = grid[r][c]
                region_cells = set()
                queue = deque([(r, c)])
                visited[r][c] = True
                
                while queue:
                    curr_r, curr_c = queue.popleft()
                    region_cells.add((curr_r, curr_c))
                    
                    # Check neighbors
                    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and grid[nr][nc] == plant_type:
                            visited[nr][nc] = True
                            queue.append((nr, nc))
                
                # Calculate area and sides
                area = len(region_cells)
                sides = count_sides(grid, region_cells)
                
                # Add to total price
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
    
    print("All samples passed!")
    
    # Solve for input.txt
    try:
        with open('input.txt', 'r') as f:
            input_text = f.read()
        
        grid = parse_input(input_text)
        result = solve_part2(grid)
        print(f"Part 2 answer: {result}")
        
    except FileNotFoundError:
        print("input.txt not found, skipping main input")

if __name__ == "__main__":
    main()
