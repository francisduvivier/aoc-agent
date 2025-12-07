from collections import deque

def solve_part2(lines):
    grid = [list(line) for line in lines]
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    
    total_price = 0
    
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    def bfs(start_r, start_c, plant_type):
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
        region_set = set(region_cells)
        sides = 0
        
        for r, c in region_cells:
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if (nr, nc) not in region_set:
                    sides += 1
        
        return sides
    
    for r in range(rows):
        for c in range(cols):
            if not visited[r][c]:
                plant_type = grid[r][c]
                region_cells = bfs(r, c, plant_type)
                area = len(region_cells)
                sides = count_sides(region_cells, plant_type)
                total_price += area * sides
    
    return total_price

sample_input = """AAAA
BBCD
BBCC
EEEC"""

sample_answer = 80

sample_result = solve_part2(sample_input.strip().splitlines())
assert sample_result == sample_answer, f"Sample result {sample_result} does not match expected {sample_answer}"
print(f"---- Sample Solution Part 2: {sample_result} ----")

with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part2(lines)
print(f"---- Final Solution Part 2: {final_result} ----")
