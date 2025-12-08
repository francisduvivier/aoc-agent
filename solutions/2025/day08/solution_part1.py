import math
import sys

def solve_part1(input_lines):
    # Parse input: each line is "x,y,z"
    junctions = []
    for line in input_lines:
        line = line.strip()
        if not line:
            continue
        x, y, z = map(int, line.split(','))
        junctions.append((x, y, z))
    
    # Union-Find (Disjoint Set Union) to track circuits
    parent = list(range(len(junctions)))
    size = [1] * len(junctions)
    
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
    
    # Compute all pairwise distances and sort by distance
    edges = []
    for i in range(len(junctions)):
        xi, yi, zi = junctions[i]
        for j in range(i + 1, len(junctions)):
            xj, yj, zj = junctions[j]
            dx = xi - xj
            dy = yi - yj
            dz = zi - zj
            dist = math.sqrt(dx*dx + dy*dy + dz*dz)
            edges.append((dist, i, j))
    
    edges.sort()
    
    # Connect the 1000 closest pairs, or all pairs if there are fewer than 1000
    connections_to_make = min(1000, len(edges))
    for dist, i, j in edges[:connections_to_make]:
        union(i, j)
    
    # Collect sizes of all circuits (only root nodes have correct sizes)
    circuit_sizes = []
    for i in range(len(junctions)):
        # Find the root of each node to get correct circuit sizes
        root = find(i)
        if root == i:  # Only count root nodes
            circuit_sizes.append(size[i])
    
    circuit_sizes.sort(reverse=True)
    
    # Multiply sizes of three largest circuits
    if len(circuit_sizes) < 3:
        result = 0
    else:
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
]  # TODO: fill with actual samples and expected results

for idx, (sample_input_lines, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part1(sample_input_lines)
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 1: {sample_result} ----") # YOU MUST NOT change this output format

# Run on the real puzzle input
final_result = solve_part1(open('input.txt').readlines())
print(f"---- Final result Part 1: {final_result} ----") # YOU MUST NOT change this output format

