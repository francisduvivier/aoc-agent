from collections import deque

def solve_part2(lines):
    # Find start position
    start = None
    for r, row in enumerate(lines):
        if 'S' in row:
            start = (r, row.index('S'))
            break
    
    # BFS to explore all possible paths
    # Each queue element is (row, col, path_count)
    # path_count tracks how many timelines reach this position
    queue = deque([start])
    # visited tracks the total number of timelines that have reached each position
    visited = {start: 1}
    
    while queue:
        r, c = queue.popleft()
        current_timelines = visited[(r, c)]
        
        # If we're at the bottom row, this position contributes to final timelines
        if r == len(lines) - 1:
            continue
            
        # Check if current position is a splitter
        if lines[r][c] == '^':
            # From a splitter, go left and right
            for dc in [-1, 1]:
                nr, nc = r + 1, c + dc
                if 0 <= nr < len(lines) and 0 <= nc < len(lines[0]):
                    if (nr, nc) not in visited:
                        visited[(nr, nc)] = current_timelines
                        queue.append((nr, nc))
                    else:
                        visited[(nr, nc)] += current_timelines
        else:
            # Continue downward
            nr, nc = r + 1, c
            if 0 <= nr < len(lines) and 0 <= nc < len(lines[0]):
                if (nr, nc) not in visited:
                    visited[(nr, nc)] = current_timelines
                    queue.append((nr, nc))
                else:
                    visited[(nr, nc)] += current_timelines
    
    # Sum timelines that reach the bottom row
    timelines = 0
    for (r, c), count in visited.items():
        if r == len(lines) - 1:
            timelines += count
    
    return timelines

# Sample data from the problem statement
samples = [
(""".......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............""", 40)
]

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part2(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 2: {sample_result} ----")

# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part2(lines)
print(f"---- Final result Part 2: {final_result} ----")
