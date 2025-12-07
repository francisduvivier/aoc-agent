import sys
from collections import deque

def read_input():
    try:
        with open('input.txt', 'r') as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print("Error: input.txt not found", file=sys.stderr)
        sys.exit(1)

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

def flood_fill(grid, start_r, start_c, visited, plant_type):
    rows, cols = len(grid), len(grid[0])
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

def get_region_sides(grid, region_cells):
    # For each cell in the region, check its 4 sides
    # A side is part of the perimeter if it's on the map boundary or adjacent to a different plant type
    sides = []
    
    for r, c in region_cells:
        plant_type = grid[r][c]
        rows, cols = len(grid), len(grid[0])
        
        # Check each of the 4 sides
        # Top side
        if r == 0 or grid[r-1][c] != plant_type:
            sides.append(('top', r, c))
        
        # Bottom side
        if r == rows - 1 or grid[r+1][c] != plant_type:
            sides.append(('bottom', r, c))
        
        # Left side
        if c == 0 or grid[r][c-1] != plant_type:
            sides.append(('left', r, c))
        
        # Right side
        if c == cols - 1 or grid[r][c+1] != plant_type:
            sides.append(('right', r, c))
    
    # Group sides by direction and merge adjacent sides
    total_sides = 0
    
    # Group by direction
    for direction in ['top', 'bottom', 'left', 'right']:
        direction_sides = [s for s in sides if s[0] == direction]
        
        if not direction_sides:
            continue
            
        # Sort sides based on direction
        if direction in ['top', 'bottom']:
            # For top/bottom, sort by column (c), then row (r)
            direction_sides.sort(key=lambda x: (x[1], x[2]))
        else:
            # For left/right, sort by row (r), then column (c)
            direction_sides.sort(key=lambda x: (x[2], x[1]))
        
        # Merge adjacent sides
        merged = []
        for side in direction_sides:
            if not merged:
                merged.append(side)
            else:
                last = merged[-1]
                # Check if this side is adjacent to the last one
                if direction == 'top':
                    # Adjacent if same row and consecutive columns
                    if side[1] == last[1] and side[2] == last[2] + 1:
                        # Extend the last side (we'll count it as one side)
                        continue
                elif direction == 'bottom':
                    # Adjacent if same row and consecutive columns
                    if side[1] == last[1] and side[2] == last[2] + 1:
                        continue
                elif direction == 'left':
                    # Adjacent if same column and consecutive rows
                    if side[2] == last[2] and side[1] == last[1] + 1:
                        continue
                elif direction == 'right':
                    # Adjacent if same column and consecutive rows
                    if side[2] == last[2] and side[1] == last[1] + 1:
                        continue
                
                # Not adjacent, add as new side
                merged.append(side)
        
        total_sides += len(merged)
    
    return total_sides

def solve():
    grid = read_input()
    if not grid:
        return
    
    rows, cols = len(grid), len(grid[0])
    visited = set()
    total_price = 0
    
    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                plant_type = grid[r][c]
                region_cells = flood_fill(grid, r, c, visited, plant_type)
                
                area = len(region_cells)
                sides = get_region_sides(grid, region_cells)
                price = area * sides
                
                total_price += price
    
    print(total_price)

if __name__ == "__main__":
    solve()
