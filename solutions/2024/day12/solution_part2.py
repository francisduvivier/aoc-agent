from collections import deque

def solve_part2(lines):
    grid = [list(line) for line in lines]
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    total_price = 0

    def get_neighbors(r, c):
        return [(nr, nc) for nr, nc in [(r-1,c), (r+1,c), (r,c-1), (r,c+1)] if 0 <= nr < rows and 0 <= nc < cols]

    def flood_fill(r, c, plant):
        region = []
        q = deque([(r, c)])
        visited[r][c] = True
        while q:
            cr, cc = q.popleft()
            region.append((cr, cc))
            for nr, nc in get_neighbors(cr, cc):
                if not visited[nr][nc] and grid[nr][nc] == plant:
                    visited[nr][nc] = True
                    q.append((nr, nc))
        return region

    def count_sides(region):
        # For each direction, count straight segments
        # Represent edges as (r, c, dir) where dir: 0=up,1=right,2=down,3=left
        edges = set()
        for r, c in region:
            # Check each side of this cell
            # Top edge (r, c, 0)
            if r == 0 or grid[r-1][c] != plant:
                edges.add((r, c, 0))
            # Bottom edge (r, c, 2)
            if r == rows-1 or grid[r+1][c] != plant:
                edges.add((r, c, 2))
            # Left edge (r, c, 3)
            if c == 0 or grid[r][c-1] != plant:
                edges.add((r, c, 3))
            # Right edge (r, c, 1)
            if c == cols-1 or grid[r][c+1] != plant:
                edges.add((r, c, 1))

        # Count connected segments for each direction
        sides = 0
        # Group edges by direction
        by_dir = {0: [], 1: [], 2: [], 3: []}
        for r, c, d in edges:
            by_dir[d].append((r, c))

        # For horizontal edges (top/bottom), merge adjacent ones in same row
        for d in [0, 2]:  # top/bottom
            by_row = {}
            for r, c in by_dir[d]:
                by_row.setdefault(r, []).append(c)
            for row_cols in by_row.values():
                row_cols.sort()
                # Count segments
                segments = 1 if row_cols else 0
                for i in range(1, len(row_cols)):
                    if row_cols[i] != row_cols[i-1] + 1:
                        segments += 1
                sides += segments

        # For vertical edges (left/right), merge adjacent ones in same col
        for d in [1, 3]:  # right/left
            by_col = {}
            for r, c in by_dir[d]:
                by_col.setdefault(c, []).append(r)
            for col_rows in by_col.values():
                col_rows.sort()
                segments = 1 if col_rows else 0
                for i in range(1, len(col_rows)):
                    if col_rows[i] != col_rows[i-1] + 1:
                        segments += 1
                sides += segments

        return sides

    for r in range(rows):
        for c in range(cols):
            if not visited[r][c]:
                plant = grid[r][c]
                region = flood_fill(r, c, plant)
                area = len(region)
                sides = count_sides(region)
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
