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
                q = deque([(i, j)])
                visited[i][j] = True
                region_cells = set()
                
                while q:
                    x, y = q.popleft()
                    region_cells.add((x, y))
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and not visited[nx][ny] and grid[nx][ny] == char:
                            visited[nx][ny] = True
                            q.append((nx, ny))
                
                area = len(region_cells)
                corners = 0
                
                for x, y in region_cells:
                    for dx, dy in [(0, 0), (0, 1), (1, 0), (1, 1)]:
                        nx, ny = x + dx, y + dy
                        if (nx, ny) not in region_cells:
                            count = 0
                            for ddx, ddy in [(0, 0), (0, -1), (-1, 0), (-1, -1)]:
                                cx, cy = nx + ddx, ny + ddy
                                if (cx, cy) in region_cells:
                                    count += 1
                            if count == 0:
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
