import sys
from collections import deque

def parse_input(filename):
    with open(filename, 'r') as f:
        return [list(line.strip()) for line in f]

def count_accessible(grid):
    rows, cols = len(grid), len(grid[0])
    accessible = []
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '@':
                # Count adjacent '@' symbols
                count = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '@':
                            count += 1
                if count < 4:
                    accessible.append((r, c))
    return accessible

def solve():
    grid = parse_input('input.txt')
    
    # Count total '@' symbols initially
    total_removed = 0
    rows, cols = len(grid), len(grid[0])
    
    # Use a queue to process removable '@' symbols
    queue = deque()
    
    # First pass: find all initially accessible '@' symbols
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '@':
                # Check if accessible
                count = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '@':
                            count += 1
                if count < 4:
                    queue.append((r, c))
    
    # Process removable '@' symbols
    while queue:
        r, c = queue.popleft()
        
        # Double-check it's still '@' and accessible (might have been processed already)
        if grid[r][c] != '@':
            continue
            
        # Count adjacent '@' symbols again
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '@':
                    count += 1
        
        if count < 4:
            # Remove this '@'
            grid[r][c] = '.'  # Mark as removed
            total_removed += 1
            
            # Check neighbors - they might now be accessible
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '@':
                        # Check if this neighbor is now accessible
                        neighbor_count = 0
                        for ndr in [-1, 0, 1]:
                            for ndc in [-1, 0, 1]:
                                if ndr == 0 and ndc == 0:
                                    continue
                                nnr, nnc = nr + ndr, nc + ndc
                                if 0 <= nnr < rows and 0 <= nnc < cols and grid[nnr][nnc] == '@':
                                    neighbor_count += 1
                        if neighbor_count < 4:
                            queue.append((nr, nc))
    
    print(total_removed)

if __name__ == '__main__':
    solve()
