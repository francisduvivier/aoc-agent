from collections import deque

def solve_part2(lines):
    if not lines or not lines[0]:
        return 0
        
    rows, cols = len(lines), len(lines[0])
    visited = set()
    total_price = 0
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    for i in range(rows):
        for j in range(cols):
            if (i, j) in visited:
                continue
                
            plant_type = lines[i][j]
            queue = deque([(i, j)])
            region_cells = set()
            region_cells.add((i, j))
            visited.add((i, j))
            
            while queue:
                x, y = queue.popleft()
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols and lines[nx][ny] == plant_type and (nx, ny) not in region_cells:
                        region_cells.add((nx, ny))
                        visited.add((nx, ny))
                        queue.append((nx, ny))
            
            area = len(region_cells)
            sides = 0
            
            for x, y in region_cells:
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if nx < 0 or nx >= rows or ny < 0 or ny >= cols or lines[nx][ny] != plant_type:
                        sides += 1
            
            corners = 0
            for x, y in region_cells:
                neighbors = []
                for dx, dy in [(0,0), (0,1), (1,0), (1,1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx <= rows and 0 <= ny <= cols:
                        if (nx < rows and ny < cols and (nx, ny) in region_cells):
                            neighbors.append(1)
                        else:
                            neighbors.append(0)
                if neighbors == [1,0,0,0] or neighbors == [0,1,0,0] or neighbors == [0,0,1,0] or neighbors == [0,0,0,1]:
                    corners += 1
                elif neighbors == [1,1,0,0] or neighbors == [0,1,1,0] or neighbors == [0,0,1,1] or neighbors == [1,0,0,1]:
                    corners += 2
                elif neighbors == [1,0,1,0] or neighbors == [0,1,0,1]:
                    corners += 0
                elif neighbors == [1,1,1,0] or neighbors == [0,1,1,1] or neighbors == [1,0,1,1] or neighbors == [1,1,0,1]:
                    corners += 2
                elif neighbors == [1,1,1,1]:
                    corners += 4
                else:
                    corners += 1
            
            total_price += area * corners
            
    return total_price

# Sample data
sample_input = """AAAA
BBCD
BBCC
EEEC"""
expected_sample_result = 80

# Run on the sample
sample_result = solve_part2(sample_input.strip().splitlines())
print(f"---- Sample Solution Part 2: {sample_result} ----")

# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part2(lines)
print(f"---- Final Solution Part 2: {final_result} ----")
