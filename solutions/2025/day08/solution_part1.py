import math
import sys

def solve_part1(input_lines):
    # Parse coordinates from input
    coords = []
    for line in input_lines:
        line = line.strip()
        if not line:
            continue
        x, y, z = map(int, line.split(','))
        coords.append((x, y, z))
    
    # Union-Find (Disjoint Set Union) structure
    parent = list(range(len(coords)))
    size = [1] * len(coords)
    
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
    for i in range(len(coords)):
        for j in range(i + 1, len(coords)):
            x1, y1, z1 = coords[i]
            x2, y2, z2 = coords[j]
            dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
            distances.append((dist, i, j))
    
    # Sort by distance and connect the 1000 closest pairs
    distances.sort()
    for dist, i, j in distances[:1000]:
        union(i, j)
    
    # Find sizes of all circuits
    circuit_sizes = []
    for i in range(len(coords)):
        if parent[i] == i:  # Root of a circuit
            circuit_sizes.append(size[i])
    
    # Sort sizes in descending order and multiply the three largest
    circuit_sizes.sort(reverse=True)
    result = circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]
    return result

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples.
samples = [
    ([
        "162,817,812",
        "57,618,57",
        "906,360,560",
        "592,479,940",
        "352,342,300",
        "466,668,158",
        "542,29,236",
        "431,825,988",
        "739,650,466",
        "52,470,668",
        "216,146,977",
        "819,987,18",
        "117,168,530",
        "805,96,715",
        "346,949,466",
        "970,615,88",
        "941,993,340",
        "862,61,35",
        "984,92,344",
        "425,690,689"
    ], 40)
]

for idx, (sample_input_lines, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part1(sample_input_lines)
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 1: {sample_result} ----") # YOU MUST NOT change this output format

# Run on the real puzzle input
final_result = solve_part1(open('input.txt').readlines())
print(f"---- Final result Part 1: {final_result} ----") # YOU MUST NOT change this output format
