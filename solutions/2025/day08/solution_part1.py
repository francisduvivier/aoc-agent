import math
from collections import defaultdict

def solve_part1(lines):
    # Parse coordinates
    coords = []
    for line in lines:
        x, y, z = map(int, line.split(','))
        coords.append((x, y, z))
    
    # Union-Find for tracking circuits
    parent = list(range(len(coords)))
    size = [1] * len(coords)
    
    def find(i):
        if parent[i] != i:
            parent[i] = find(parent[i])
        return parent[i]
    
    def union(i, j):
        ri, rj = find(i), find(j)
        if ri != rj:
            if size[ri] < size[rj]:
                parent[ri] = rj
                size[rj] += size[ri]
            else:
                parent[rj] = ri
                size[ri] += size[rj]
    
    # Compute distances and sort
    distances = []
    for i in range(len(coords)):
        for j in range(i + 1, len(coords)):
            x1, y1, z1 = coords[i]
            x2, y2, z2 = coords[j]
            dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
            distances.append((dist, i, j))
    
    distances.sort()
    
    # Connect 1000 closest pairs
    for dist, i, j in distances[:1000]:
        union(i, j)
    
    # Find circuit sizes
    circuit_sizes = []
    for i in range(len(coords)):
        if parent[i] == i:
            circuit_sizes.append(size[i])
    
    circuit_sizes.sort(reverse=True)
    
    # Multiply sizes of three largest circuits
    result = circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]
    return result

# Sample data from problem statement
samples = [
    ("""162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689""", 40)
]

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part1(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 1: {sample_result} ----")

# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part1(lines)
print(f"---- Final result Part 1: {final_result} ----")
