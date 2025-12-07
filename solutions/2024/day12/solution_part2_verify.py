# Edit this file: implement solve_part2

def solve_part2(lines):
    # Parse grid
    grid = [list(line) for line in lines]
    rows, cols = len(grid), len(grid[0])
    
    # Union-Find to group adjacent same-type cells
    parent = {}
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[py] = px
    
    # Initialize and union neighbors
    for r in range(rows):
        for c in range(cols):
            parent[(r, c)] = (r, c)
    for r in range(rows):
        for c in range(cols):
            if r + 1 < rows and grid[r][c] == grid[r + 1][c]:
                union((r, c), (r + 1, c))
            if c + 1 < cols and grid[r][c] == grid[r][c + 1]:
                union((r, c), (r, c + 1))
    
    # Group cells by region root
    regions = {}
    for r in range(rows):
        for c in range(cols):
            root = find((r, c))
            if root not in regions:
                regions[root] = []
            regions[root].append((r, c))
    
    total_price = 0
    for cells in regions.values():
        # Area
        area = len(cells)
        plant_type = grid[cells[0][0]][cells[0][1]]
        
        # Compute sides by counting straight segments along the boundary
        # Represent edges as (r, c, dir) where dir: 0=up, 1=right, 2=down, 3=left
        # For each cell, add outward edges not adjacent to same region
        outward_edges = set()
        cell_set = set(cells)
        for r, c in cells:
            # Up edge
            if (r - 1, c) not in cell_set:
                outward_edges.add((r, c, 0))
            # Right edge
            if (r, c + 1) not in cell_set:
                outward_edges.add((r, c, 1))
            # Down edge
            if (r + 1, c) not in cell_set:
                outward_edges.add((r, c, 2))
            # Left edge
            if (r, c - 1) not in cell_set:
                outward_edges.add((r, c, 3))
        
        # Merge adjacent edges to count sides
        # Group edges by direction and then merge contiguous segments
        sides = 0
        for direction in range(4):
            edges_dir = [(r, c) for (r, c, d) in outward_edges if d == direction]
            if not edges_dir:
                continue
            # Sort edges for merging
            if direction in (0, 2):  # horizontal edges (up/down): sort by c then r
                edges_dir.sort(key=lambda x: (x[1], x[0]))
                # Merge contiguous in column direction
                merged = []
                for r, c in edges_dir:
                    if not merged:
                        merged.append([r, r, c])
                    else:
                        last = merged[-1]
                        if c == last[2] and r == last[1] + 1:
                            last[1] = r
                        else:
                            merged.append([r, r, c])
                sides += len(merged)
            else:  # vertical edges (right/left): sort by r then c
                edges_dir.sort(key=lambda x: (x[0], x[1]))
                merged = []
                for r, c in edges_dir:
                    if not merged:
                        merged.append([c, c, r])
                    else:
                        last = merged[-1]
                        if r == last[2] and c == last[1] + 1:
                            last[1] = c
                        else:
                            merged.append([c, c, r])
                sides += len(merged)
        
        total_price += area * sides
    
    return total_price

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples.
samples = [
    ("AAAA\nBBCD\nBBCC\nEEEC", 80),
    ("OOOOO\nOXOXO\nOOOOO\nOXOXO\nOOOOO", 436),
    ("EEEEE\nEXXXX\nEEEEE\nEXXXX\nEEEEE", 236),
    ("AAAAAA\nAAABBA\nAAABBA\nABBAAA\nABBAAA\nAAAAAA", 368),
    ("RRRRIICCFF\nRRRRIICCCF\nVVRRRCCFFF\nVVRCCCJFFF\nVVVVCJJCFE\nVVIVCCJJEE\nVVIIICJJEE\nMIIIIIJJEE\nMIIISIJEEE\nMMMISSJEEE", 1206)
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

