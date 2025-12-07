from collections import deque

def solve_part2(lines):
    grid = [list(line) for line in lines]
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    
    total_price = 0
    
    # Directions: up, right, down, left
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    def bfs(start_r, start_c, plant_type):
        """BFS to find all connected cells of same type"""
        queue = deque([(start_r, start_c)])
        visited[start_r][start_c] = True
        region_cells = []
        
        while queue:
            r, c = queue.popleft()
            region_cells.append((r, c))
            
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and grid[nr][nc] == plant_type:
                    visited[nr][nc] = True
                    queue.append((nr, nc))
        
        return region_cells
    
    def count_sides(region_cells, plant_type):
        """Count the number of sides for a region"""
        # Create a set for faster lookup
        region_set = set(region_cells)
        
        # We'll trace the boundary and count continuous segments
        # First, find all boundary edges
        boundary_edges = set()
        
        for r, c in region_cells:
            # Check each direction
            for i, (dr, dc) in enumerate(dirs):
                nr, nc = r + dr, c + dc
                # If neighbor is out of bounds or different type, this is a boundary
                if not (0 <= nr < rows and 0 <= nc < cols) or grid[nr][nc] != plant_type:
                    # Store the edge as (r, c, direction)
                    boundary_edges.add((r, c, i))
        
        # Now we need to connect continuous boundary segments
        visited_edges = set()
        side_count = 0
        
        for edge in boundary_edges:
            if edge in visited_edges:
                continue
                
            # Start a new side
            side_count += 1
            queue = deque([edge])
            visited_edges.add(edge)
            
            while queue:
                r, c, dir_idx = queue.popleft()
                
                # Try to extend in both directions along the boundary
                for offset in [-1, 1]:
                    # Get adjacent edge in the boundary
                    new_dir = (dir_idx + offset) % 4
                    
                    # Calculate position of adjacent edge
                    if offset == -1:  # Counter-clockwise
                        # Move to adjacent cell along the boundary
                        adj_r, adj_c = r, c
                        if new_dir == 0: adj_r -= 1
                        elif new_dir == 1: adj_c += 1  
                        elif new_dir == 2: adj_r += 1
                        elif new_dir == 3: adj_c -= 1
                    else:  # Clockwise  
                        adj_r, adj_c = r, c
                        if dir_idx == 0: adj_c -= 1
                        elif dir_idx == 1: adj_r -= 1
                        elif dir_idx == 2: adj_c += 1
                        elif dir_idx == 3: adj_r += 1
                    
                    # Check if this adjacent edge exists and is part of the same boundary
                    if (adj_r, adj_c, new_dir) in boundary_edges and (adj_r, adj_c, new_dir) not in visited_edges:
                        visited_edges.add((adj_r, adj_c, new_dir))
                        queue.append((adj_r, adj_c, new_dir))
        
        return side_count
    
    # Process all regions
    for r in range(rows):
        for c in range(cols):
            if not visited[r][c]:
                plant_type = grid[r][c]
                region_cells = bfs(r, c, plant_type)
                area = len(region_cells)
                sides = count_sides(region_cells, plant_type)
                total_price += area * sides
    
    return total_price

# Sample data from problem statement
sample_input = """AAAA
BBCD
BBCC
EEEC"""

sample_answer = 80  # From the problem: 16 + 16 + 32 + 4 + 12 = 80

# Run on the sample and verify
sample_result = solve_part2(sample_input.strip().splitlines())
assert sample_result == sample_answer, f"Sample result {sample_result} does not match expected {sample_answer}"
print(f"---- Sample Solution Part 2: {sample_result} ----")

# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part2(lines)
print(f"---- Final Solution Part 2: {final_result} ----")
