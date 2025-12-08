import sys
import math
from collections import defaultdict

def solve_part1(lines):
    # Parse input
    junctions = []
    for line in lines:
        if line.strip():
            x, y, z = map(int, line.strip().split(','))
            junctions.append((x, y, z))
    
    # Calculate distances between all pairs
    distances = []
    n = len(junctions)
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1, z1 = junctions[i]
            x2, y2, z2 = junctions[j]
            dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
            distances.append((dist, i, j))
    
    # Sort by distance
    distances.sort()
    
    # Union-Find for circuit tracking
    parent = list(range(n))
    size = [1] * n
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry:
            if size[rx] < size[ry]:
                parent[rx] = ry
                size[ry] += size[rx]
            else:
                parent[ry] = rx
                size[rx] += size[ry]
    
    # Connect 1000 closest pairs
    connections_made = 0
    for dist, i, j in distances:
        if connections_made >= 1000:
            break
        if find(i) != find(j):
            union(i, j)
            connections_made += 1
    
    # Get circuit sizes
    circuit_sizes = []
    for i in range(n):
        if parent[i] == i:  # Root of a circuit
            circuit_sizes.append(size[i])
    
    # Sort and multiply top 3
    circuit_sizes.sort(reverse=True)
    return circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]

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
