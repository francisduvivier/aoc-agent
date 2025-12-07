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
                region_cells = []
                
                while q:
                    x, y = q.popleft()
                    area += 1
                    region_cells.append((x, y))
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
                
                total_price += area * sides
    
    return total_price

# Sample data from the problem statement
sample_input = """AAAA
BBCD
BBCC
EEEC"""
expected_sample_result = 80

# Run on the sample and verify
sample_result = solve_part2(sample_input.strip().splitlines())
assert sample_result == expected_sample_result, f"Sample result {sample_result} does not match expected {expected_sample_result}"
print(f"---- Sample Solution Part 2: {sample_result} ----")

# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part2(lines)
print(f"---- Final Solution Part 2: {final_result} ----")
