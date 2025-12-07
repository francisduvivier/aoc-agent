from collections import deque

def solve_part2(lines):
    if not lines or not lines[0]:
        return 0
        
    grid = [list(line.strip()) for line in lines if line.strip()]
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    total_price = 0
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    for i in range(rows):
        for j in range(cols):
            if not visited[i][j]:
                char = grid[i][j]
                q = deque([(i, j)])
                visited[i][j] = True
                region_cells = set()
                region_cells.add((i, j))
                
                while q:
                    x, y = q.popleft()
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and grid[nx][ny] == char:
                            visited[nx][ny] = True
                            q.append((nx, ny))
                            region_cells.add((nx, ny))
                
                area = len(region_cells)
                
                corners = set()
                for x, y in region_cells:
                    corners.add((x, y))
                    corners.add((x, y+1))
                    corners.add((x+1, y))
                    corners.add((x+1, y+1))
                
                sides = 0
                for corner in corners:
                    x, y = corner
                    adjacent_cells = [(x-1, y-1), (x-1, y), (x, y-1), (x, y)]
                    count_in_region = sum(1 for cell in adjacent_cells if cell in region_cells)
                    if count_in_region % 2 == 1:
                        sides += 1
                
                total_price += area * sides
    
    return total_price

sample_input = """AAAA
BBCD
BBCC
EEEC"""
sample_answer = 80

sample_result = solve_part2(sample_input.strip().splitlines())
assert sample_result == sample_answer, f"Sample result {sample_result} does not match expected {sample_answer}"

with open('input.txt') as f:
    lines = f.readlines()

result = solve_part2(lines)
print(result)
