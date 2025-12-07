from collections import deque

def solve_part2(lines):
    grid = [list(line) for line in lines]
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    total_price = 0
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    for i in range(rows):
        for j in range(cols):
            if not visited[i][j]:
                char = grid[i][j]
                area = 0
                q = deque([(i, j)])
                visited[i][j] = True
                region_cells = set()
                
                while q:
                    x, y = q.popleft()
                    area += 1
                    region_cells.add((x, y))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and grid[nx][ny] == char:
                            visited[nx][ny] = True
                            q.append((nx, ny))
                
                sides = 0
                for x, y in region_cells:
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if not (0 <= nx < rows and 0 <= ny < cols) or grid[nx][ny] != char:
                            sides += 1
                
                corners = 0
                for x, y in region_cells:
                    for dx1, dy1 in [(0, 0), (0, 1), (1, 0), (1, 1)]:
                        has_cell = (x + dx1, y + dy1) in region_cells
                        has_outside = False
                        for dx2, dy2 in [(0, 0), (0, -1), (-1, 0), (-1, -1)]:
                            nx, ny = x + dx1 + dx2, y + dy1 + dy2
                            if not (0 <= nx < rows and 0 <= ny < cols) or grid[nx][ny] != char:
                                has_outside = True
                                break
                        if has_outside and not has_cell:
                            corners += 1
                
                total_price += area * corners
    
    return total_price

sample_input = """AAAA
BBCD
BBCC
EEEC"""
expected_sample_result = 80

sample_result = solve_part2(sample_input.strip().splitlines())
assert sample_result == expected_sample_result, f"Sample result {sample_result} does not match expected {expected_sample_result}"
print(f"---- Sample Solution Part 2: {sample_result} ----")

with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part2(lines)
print(f"---- Final Solution Part 2: {final_result} ----")
