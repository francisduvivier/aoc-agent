import math

def solve_part1(input_lines, config):
    # Parse 3D coordinates from input
    junctions = []
    for line in input_lines:
        line = line.strip()
        if line:
            x, y, z = map(int, line.split(','))
            junctions.append((x, y, z))
    
    # Calculate Euclidean distance between two junctions
    def distance(a, b):
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2)
    
    # Create list of all possible connections with distances
    connections = []
    n = len(junctions)
    for i in range(n):
        for j in range(i + 1, n):
            dist = distance(junctions[i], junctions[j])
            connections.append((dist, i, j))
    
    # Sort connections by distance (shortest first)
    connections.sort()
    
    # Union-Find data structure to track circuits
    parent = list(range(n))
    size = [1] * n
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        root_x = find(x)
        root_y = find(y)
        if root_x != root_y:
            if size[root_x] < size[root_y]:
                parent[root_x] = root_y
                size[root_y] += size[root_x]
                size[root_x] = 0
            else:
                parent[root_y] = root_x
                size[root_x] += size[root_y]
                size[root_y] = 0
    
    # Connect the 1000 closest pairs, but not more than available connections
    connections_made = 0
    max_connections = min(1000, len(connections))
    for dist, i, j in connections:
        if connections_made >= max_connections:
            break
        union(i, j)
        connections_made += 1
    
    # Get circuit sizes and find the three largest
    circuit_sizes = sorted([s for s in size if s > 0], reverse=True)
    
    # Multiply the three largest circuits, handling case where there are fewer than 3
    # If fewer than 3 circuits, multiply available circuits by 1 for missing ones
    result = 1
    for i in range(min(3, len(circuit_sizes))):
        result *= circuit_sizes[i]
    
    return result

# Sample data from problem statement
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
    sample_config = "TODO"
    sample_result = solve_part1(sample_input_lines, sample_config)
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 1: {sample_result} ----")

# Run on the real puzzle input
final_config = "TODO"
final_result = solve_part1(open('input.txt').readlines(), final_config)
print(f"---- Final result Part 1: {final_result} ----")
