from collections import deque

def solve_part2(lines):
    grid = [list(line) for line in lines]
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    total_price = 0

    def get_neighbors(r, c):
        return [(nr, nc) for nr, nc in [(r-1,c), (r+1,c), (r,c-1), (r,c+1)] 
                if 0 <= nr < rows and 0 <= nc < cols]

    def bfs(r, c, plant_type):
        queue = deque([(r, c)])
        visited[r][c] = True
        region_cells = []
        while queue:
            cr, cc = queue.popleft()
            region_cells.append((cr, cc))
            for nr, nc in get_neighbors(cr, cc):
                if not visited[nr][nc] and grid[nr][nc] == plant_type:
                    visited[nr][nc] = True
                    queue.append((nr, nc))
        return region_cells

    def count_sides(cells):
        # Create a set of region cells for fast lookup
        region_set = set(cells)
        
        # For each direction, count straight segments
        sides = 0
        
        # Horizontal segments (top/bottom edges)
        for r, c in cells:
            # Check top edge
            if (r-1, c) not in region_set:
                # Extend segment to the left
                left = c
                while left > 0 and (r, left-1) in region_set and (r-1, left-1) not in region_set:
                    left -= 1
                # Extend segment to the right
                right = c
                while right < cols-1 and (r, right+1) in region_set and (r-1, right+1) not in region_set:
                    right += 1
                # Count this as one side if it's the leftmost cell of this segment
                if c == left:
                    sides += 1
            
            # Check bottom edge
            if (r+1, c) not in region_set:
                # Extend segment to the left
                left = c
                while left > 0 and (r, left-1) in region_set and (r+1, left-1) not in region_set:
                    left -= 1
                # Extend segment to the right
                right = c
                while right < cols-1 and (r, right+1) in region_set and (r+1, right+1) not in region_set:
                    right += 1
                # Count this as one side if it's the leftmost cell of this segment
                if c == left:
                    sides += 1
        
        # Vertical segments (left/right edges)
        for r, c in cells:
            # Check left edge
            if (r, c-1) not in region_set:
                # Extend segment upward
                up = r
                while up > 0 and (up-1, c) in region_set and (up-1, c-1) not in region_set:
                    up -= 1
                # Extend segment downward
                down = r
                while down < rows-1 and (down+1, c) in region_set and (down+1, c-1) not in region_set:
                    down += 1
                # Count this as one side if it's the topmost cell of this segment
                if r == up:
                    sides += 1
            
            # Check right edge
            if (r, c+1) not in region_set:
                # Extend segment upward
                up = r
                while up > 0 and (up-1, c) in region_set and (up-1, c+1) not in region_set:
                    up -= 1
                # Extend segment downward
                down = r
                while down < rows-1 and (down+1, c) in region_set and (down+1, c+1) not in region_set:
                    down += 1
                # Count this as one side if it's the topmost cell of this segment
                if r == up:
                    sides += 1
        
        return sides

    for r in range(rows):
        for c in range(cols):
            if not visited[r][c]:
                plant_type = grid[r][c]
                region_cells = bfs(r, c, plant_type)
                area = len(region_cells)
                sides = count_sides(region_cells)
                total_price += area * sides

    return total_price

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples.
samples = [
    ("""AAAA
BBCD
BBCC
EEEC""", 80),
    ("""OOOOO
OXOXO
OOOOO
OXOXO
OOOOO""", 436),
    ("""EEEEE
EXXXX
EEEEE
EXXXX
EEEEE""", 236),
    ("""AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA""", 368),
    ("""RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE""", 1206)
]  # TODO: fill with actual samples and expected results

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part2(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 2: {sample_result} ----") # YOU MUST NOT change this output format

# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part2(lines)
print(f"---- Final result Part 2: {final_result} ----") # YOU MUST NOT change this output format
