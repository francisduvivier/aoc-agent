import sys
from collections import deque

def solve_part1(grid):
    # Find the starting position 'S'
    start = None
    for r, row in enumerate(grid):
        if 'S' in row:
            start = (r, row.index('S'))
            break
    
    # BFS to simulate tachyon beam propagation
    queue = deque([start])
    visited = set([start])
    splits = 0
    
    while queue:
        r, c = queue.popleft()
        
        # Move downward from current position
        nr = r + 1
        if nr >= len(grid):
            continue
            
        # Continue downward through empty space
        while nr < len(grid) and grid[nr][c] == '.':
            if (nr, c) in visited:
                break
            visited.add((nr, c))
            queue.append((nr, c))
            nr += 1
        
        # If we hit a splitter, process it
        if nr < len(grid) and grid[nr][c] == '^':
            if (nr, c) not in visited:
                visited.add((nr, c))
                splits += 1
                
                # Add left and right positions from the splitter
                for dc in [-1, 1]:
                    nc = c + dc
                    if 0 <= nc < len(grid[0]):
                        if (nr, nc) not in visited:
                            visited.add((nr, nc))
                            queue.append((nr, nc))
    
    return splits

if __name__ == '__main__':
    with open('input.txt') as f:
        lines = [line.strip() for line in f]
    print(solve_part1(lines))
