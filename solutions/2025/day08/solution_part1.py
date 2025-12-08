import math
import sys

def solve_part1(lines):
    # Parse junction box coordinates
    boxes = []
    for line in lines:
        if not line.strip():
            continue
        x, y, z = map(int, line.strip().split(','))
        boxes.append((x, y, z))
    
    # Union-Find data structure to track circuits
    parent = list(range(len(boxes)))
    size = [1] * len(boxes)
    
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
    
    # Calculate distances between all pairs
    distances = []
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            x1, y1, z1 = boxes[i]
            x2, y2, z2 = boxes[j]
            dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
            distances.append((dist, i, j))
    
    # Sort by distance and connect the 1000 closest pairs
    distances.sort()
    for dist, i, j in distances[:1000]:
        union(i, j)
    
    # Find all circuit sizes
    circuit_sizes = []
    for i in range(len(boxes)):
        if parent[i] == i:
            circuit_sizes.append(size[i])
    
    # Sort and multiply the three largest
    circuit_sizes.sort(reverse=True)
    result = 1
    for i in range(min(3, len(circuit_sizes))):
        result *= circuit_sizes[i]
    return result

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples.
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
    print(f"---- Sample {idx} result Part 1: {sample_result} ----") # YOU MUST NOT change this output format

# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part1(lines)
print(f"---- Final result Part 1: {final_result} ----") # YOU MUST NOT change this output format

