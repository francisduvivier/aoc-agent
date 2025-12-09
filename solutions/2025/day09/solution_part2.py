# Edit this file: implement solve_part2

def solve_part2(lines):
    reds = []
    for line in lines:
        x, y = map(int, line.split(','))
        reds.append((x, y))
    
    boundary = set(reds)
    for i in range(len(reds)):
        p1 = reds[i]
        p2 = reds[(i + 1) % len(reds)]
        if p1[0] == p2[0]:
            x = p1[0]
            y1, y2 = sorted([p1[1], p2[1]])
            for y in range(y1, y2 + 1):
                boundary.add((x, y))
        else:
            y = p1[1]
            x1, x2 = sorted([p1[0], p2[0]])
            for x in range(x1, x2 + 1):
                boundary.add((x, y))
    
    from collections import defaultdict
    min_x = defaultdict(lambda: float('inf'))
    max_x = defaultdict(lambda: float('-inf'))
    for x, y in boundary:
        min_x[y] = min(min_x[y], x)
        max_x[y] = max(max_x[y], x)
    
    max_area = 0
    for i in range(len(reds)):
        for j in range(i + 1, len(reds)):
            p1 = reds[i]
            p2 = reds[j]
            x1 = min(p1[0], p2[0])
            x2 = max(p1[0], p2[0])
            y1 = min(p1[1], p2[1])
            y2 = max(p1[1], p2[1])
            valid = True
            for y in range(y1, y2 + 1):
                if min_x[y] > x1 or max_x[y] < x2:
                    valid = False
                    break
            if valid:
                area = (x2 - x1 + 1) * (y2 - y1 + 1)
                max_area = max(max_area, area)
    return max_area

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples IF there are any samples given for part 2.
samples = [("7,1\n11,1\n11,7\n9,7\n9,5\n2,5\n2,3\n7,3", 24)]  # TODO: fill with actual samples and expected results

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part2(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 2: {sample_result} ----") # YOU MUST NOT change this output format
# print(f"---- Sample NONE result Part 2: NONE ----") # Uncomment this if no samples are given for part 2
# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part2(lines)
print(f"---- Final result Part 2: {final_result} ----") # YOU MUST NOT change this output format
