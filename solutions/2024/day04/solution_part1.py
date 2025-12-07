def solve_part1(lines):
    rows = len(lines)
    cols = len(lines[0]) if rows > 0 else 0
    target = "XMAS"
    count = 0
    
    # Directions: (dx, dy) for 8 directions
    directions = [
        (0, 1),   # right
        (1, 0),   # down
        (0, -1),  # left
        (-1, 0),  # up
        (1, 1),   # down-right
        (1, -1),  # down-left
        (-1, 1),  # up-right
        (-1, -1)  # up-left
    ]
    
    for r in range(rows):
        for c in range(cols):
            for dr, dc in directions:
                # Check if the word fits in this direction
                valid = True
                for i in range(len(target)):
                    nr, nc = r + dr * i, c + dc * i
                    if nr < 0 or nr >= rows or nc < 0 or nc >= cols or lines[nr][nc] != target[i]:
                        valid = False
                        break
                if valid:
                    count += 1
                    
    return count

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples.
samples = [
    ("""MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX""", 18)
]  # TODO: fill with actual samples and expected results

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part1(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 1: {sample_result} ----") # YOU MUST NOT change this output format

# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part1(lines)
print(f"---- Final result Part 1: {final_result} ----") # YOU MUST NOT change this output format
