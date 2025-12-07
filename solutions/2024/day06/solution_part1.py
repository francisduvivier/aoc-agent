# Edit this file: implement solve_part1

def solve_part1(lines):
    # Find guard position and direction
    guard_pos = None
    guard_dir = None
    directions = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}
    
    for r, line in enumerate(lines):
        for c, ch in enumerate(line):
            if ch in directions:
                guard_pos = (r, c)
                guard_dir = ch
                break
        if guard_pos:
            break
    
    # Convert grid to list of lists for easier manipulation
    grid = [list(line) for line in lines]
    visited = set()
    visited.add(guard_pos)
    
    # Simulate guard movement
    while True:
        dr, dc = directions[guard_dir]
        nr, nc = guard_pos[0] + dr, guard_pos[1] + dc
        
        # Check if next position is out of bounds
        if nr < 0 or nr >= len(grid) or nc < 0 or nc >= len(grid[0]):
            break
            
        # Check if there's an obstacle
        if grid[nr][nc] == '#':
            # Turn right 90 degrees
            dirs = ['^', '>', 'v', '<']
            current_idx = dirs.index(guard_dir)
            guard_dir = dirs[(current_idx + 1) % 4]
        else:
            # Move forward
            guard_pos = (nr, nc)
            visited.add(guard_pos)
    
    return len(visited)

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples.
samples = [
    ("""....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...""", 41)
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

