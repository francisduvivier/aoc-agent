import sys
import math
from collections import defaultdict

def solve_part1(lines):
    # Parse junction box positions
    junctions = []
    for line in lines:
        if line.strip():
            x, y, z = map(int, line.strip().split(','))
            junctions.append((x, y, z))
    
    # Union-Find data structure
    parent = list(range(len(junctions)))
    size = [1] * len(junctions)
    
    def find(i):
        if parent[i] != i:
            parent[i] = find(parent[i])
        return parent[i]
    
    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            if size[root_i] < size[root_j]:
                parent[root_i] = root_j
                size[root_j] += size[root_i]
            else:
                parent[root_j] = root_i
                size[root_i] += size[root_j]
    
    # Calculate distances and sort connections
    connections = []
    for i in range(len(junctions)):
        for j in range(i + 1, len(junctions)):
            x1, y1, z1 = junctions[i]
            x2, y2, z2 = junctions[j]
            dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
            connections.append((dist, i, j))
    
    connections.sort()
    
    # Make the 1000 shortest connections
    for dist, i, j in connections[:1000]:
        union(i, j)
    
    # Find all circuit sizes
    circuit_sizes = []
    for i in range(len(junctions)):
        if parent[i] == i:  # Root of a circuit
            circuit_sizes.append(size[i])
    
    # Sort and multiply the three largest circuits
    circuit_sizes.sort(reverse=True)
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
