import sys
from collections import deque

def read_grid(filename):
    with open(filename, 'r') as f:
        return [list(line.strip()) for line in f]

def count_accessible(grid):
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '@':
                # Count adjacent '@' in 8 directions
                adjacent_count = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '@':
                            adjacent_count += 1
                
                if adjacent_count < 4:
                    count += 1
    
    return count

def total_removable(grid):
    rows, cols = len(grid), len(grid[0])
    
    # Create a copy to work with
    work_grid = [row[:] for row in grid]
    
    total_removed = 0
    
    while True:
        # Find removable rolls
        removable = []
        for r in range(rows):
            for c in range(cols):
                if work_grid[r][c] == '@':
                    # Count adjacent '@' in 8 directions
                    adjacent_count = 0
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < rows and 0 <= nc < cols and work_grid[nr][nc] == '@':
                                adjacent_count += 1
                    
                    if adjacent_count < 4:
                        removable.append((r, c))
        
        # If no rolls can be removed, stop
        if not removable:
            break
        
        # Remove all accessible rolls
        for r, c in removable:
            work_grid[r][c] = '.'
            total_removed += 1
    
    return total_removed

def main():
    grid = read_grid('input.txt')
    
    part1 = count_accessible(grid)
    part2 = total_removable(grid)
    
    print(part1)
    print(part2)

if __name__ == '__main__':
    main()
