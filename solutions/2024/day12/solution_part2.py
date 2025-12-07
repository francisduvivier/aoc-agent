import sys
from collections import deque

def find_regions(grid):
    visited = set()
    regions = []
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    for i in range(rows):
        for j in range(cols):
            if (i, j) not in visited:
                char = grid[i][j]
                queue = deque([(i, j)])
                visited.add((i, j))
                region = []
                while queue:
                    x, y = queue.popleft()
                    region.append((x, y))
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited and grid[nx][ny] == char:
                            visited.add((nx, ny))
                            queue.append((nx, ny))
                regions.append((char, region))
    return regions

def get_edges(region, grid):
    cells = set(region)
    edges = []
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    for (i, j) in region:
        # Check top edge (cell above)
        if i == 0 or (i-1, j) not in cells:
            edges.append(('h', i, j, j+1))
        # Check right edge (cell to the right)
        if j == cols-1 or (i, j+1) not in cells:
            edges.append(('v', j+1, i, i+1))
        # Check bottom edge (cell below)
        if i == rows-1 or (i+1, j) not in cells:
            edges.append(('h', i+1, j, j+1))
        # Check left edge (cell to the left)
        if j == 0 or (i, j-1) not in cells:
            edges.append(('v', j, i, i+1))
    return edges

def merge_edges(edges):
    h_segments = {}
    v_segments = {}
    
    for edge in edges:
        if edge[0] == 'h':
            y = edge[1]
            x_start, x_end = edge[2], edge[3]
            if y not in h_segments:
                h_segments[y] = []
            h_segments[y].append((x_start, x_end))
        else:
            x = edge[1]
            y_start, y_end = edge[2], edge[3]
            if x not in v_segments:
                v_segments[x] = []
            v_segments[x].append((y_start, y_end))
    
    merged = []
    # Merge horizontal segments
    for y in h_segments:
        segs = sorted(h_segments[y], key=lambda s: s[0])
        current = segs[0]
        for seg in segs[1:]:
            if seg[0] <= current[1]:
                current = (current[0], max(current[1], seg[1]))
            else:
                merged.append(('h', y, current[0], current[1]))
                current = seg
        merged.append(('h', y, current[0], current[1]))
    
    # Merge vertical segments
    for x in v_segments:
        segs = sorted(v_segments[x], key=lambda s: s[0])
        current = segs[0]
        for seg in segs[1:]:
            if seg[0] <= current[1]:
                current = (current[0], max(current[1], seg[1]))
            else:
                merged.append(('v', x, current[0], current[1]))
                current = seg
        merged.append(('v', x, current[0], current[1]))
    
    return merged

def solve_part2(lines):
    grid = [line.strip() for line in lines]
    regions = find_regions(grid)
    total_price = 0
    for char, cells in regions:
        area = len(cells)
        edges = get_edges(cells, grid)
        merged_edges = merge_edges(edges)
        num_sides = len(merged_edges)
        price = area * num_sides
        total_price += price
    return total_price

# Samples
samples = [
    (
        [
            "AAAA",
            "BBCD",
            "BBCC",
            "EEEC"
        ],
        80
    ),
    (
        [
            "OOOOO",
            "OXOXO",
            "OOOOO",
            "OXOXO",
            "OOOOO"
        ],
        436
    ),
    (
        [
            "EEEEE",
            "EXXXX",
            "EEEEE",
            "EXXXX",
            "EEEEE"
        ],
        236
    ),
    (
        [
            "AAAAAA",
            "AAABBA",
            "AAABBA",
            "ABBAAA",
            "ABBAAA",
            "AAAAAA"
        ],
        368
    )
]

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_res = solve_part2(sample_input)
    assert sample_res == expected_result, f"Sample {idx} failed: expected {expected_result}, got {sample_res}"
    print(f"---- Sample {idx} Solution Part 2: {sample_res} ----")

# Run on real input
with open('input.txt') as f:
    lines = f.readlines()
final_result = solve_part2(lines)
print(f"---- Final Solution Part 2: {final_result} ----")
