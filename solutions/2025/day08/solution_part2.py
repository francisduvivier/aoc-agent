def solve_part2(lines):
    points = [tuple(map(int, line.strip().split(','))) for line in lines]
    n = len(points)
    if n == 0:
        return 0
    if n == 1:
        return 0  # Only one box, no pair to connect

    # Generate all pairs with squared distance to avoid floating point
    pairs = []
    for i in range(n):
        for j in range(i+1, n):
            x1, y1, z1 = points[i]
            x2, y2, z2 = points[j]
            dx = x1 - x2
            dy = y1 - y2
            dz = z1 - z2
            dist_sq = dx*dx + dy*dy + dz*dz
            pairs.append((dist_sq, i, j))

    # Sort by distance, then by i, then j for deterministic order
    pairs.sort()

    # DSU implementation
    parent = list(range(n))
    rank = [0] * n

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        xroot = find(x)
        yroot = find(y)
        if xroot == yroot:
            return False
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1
        return True

    component_count = n
    last_x_pair = None

    for dist_sq, i, j in pairs:
        if component_count == 1:
            break
        if find(i) != find(j):
            union(i, j)
            component_count -= 1
            if component_count == 1:
                # This is the last pair that connected the final components
                last_x_pair = (points[i][0], points[j][0])
                break

    if last_x_pair:
        return last_x_pair[0] * last_x_pair[1]
    return 0  # In case all points were already connected

samples = [
    (
        """162,817,812
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
425,690,689""",
        25272
    )
]

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part2(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 2: {sample_result} ----")

with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part2(lines)
print(f"---- Final result Part 2: {final_result} ----")
