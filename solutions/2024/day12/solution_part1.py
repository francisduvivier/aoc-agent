from collections import deque

def solve_part1(lines):
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
            area = 0
            perimeter = 0
            
            while queue:
                cr, cc = queue.popleft()
                area += 1
                
                for dr, dc in directions:
                    nr, nc = cr + dr, cc + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if grid[nr][nc] == plant_type:
                            if (nr, nc) not in visited:
                                visited.add((nr, nc))
                                queue.append((nr, nc))
                        else:
                            perimeter += 1
                    else:
                        perimeter += 1
            
            total_price += area * perimeter
    
    return total_price

if __name__ == '__main__':
    sample_input = """AAAA
BBCD
BBCC
EEEC"""
    
    expected_sample_result = 140

    sample_result = solve_part1(sample_input.strip().splitlines())
    print(f"---- Sample Solution Part 1: {sample_result} ----")

    with open('input.txt') as f:
        lines = [line.strip() for line in f]
    final_result = solve_part1(lines)
    print(f"---- Final Solution Part 1: {final_result} ----")
