def solve_part2(lines):
    # Parse grid and find guard start position
    grid = [list(line) for line in lines]
    rows, cols = len(grid), len(grid[0])
    
    # Find guard start position
    start_r, start_c = None, None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '^':
                start_r, start_c = r, c
                break
        if start_r is not None:
            break
    
    # Define directions: 0=up, 1=right, 2=down, 3=left
    dr = [-1, 0, 1, 0]
    dc = [0, 1, 0, -1]
    
    def simulate_with_obstacle(ob_r, ob_c):
        # Create grid with obstacle
        test_grid = [row[:] for row in grid]
        if ob_r is not None:
            test_grid[ob_r][ob_c] = '#'
        
        # Simulate guard movement
        r, c = start_r, start_c
        d = 0  # Start facing up
        visited = set()
        
        while 0 <= r < rows and 0 <= c < cols:
            state = (r, c, d)
            if state in visited:
                return True  # Loop detected
            visited.add(state)
            
            # Check next position
            nr, nc = r + dr[d], c + dc[d]
            
            # If next position is out of bounds, guard leaves
            if not (0 <= nr < rows and 0 <= nc < cols):
                return False
            
            # If obstacle in front, turn right
            if test_grid[nr][nc] == '#':
                d = (d + 1) % 4
            else:
                # Move forward
                r, c = nr, nc
        
        return False  # Guard left the area
    
    # Count valid obstacle positions (excluding start position)
    count = 0
    for r in range(rows):
        for c in range(cols):
            if (r, c) != (start_r, start_c) and grid[r][c] == '.':
                if simulate_with_obstacle(r, c):
                    count += 1
    
    return count

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
......#...""", 6)
]  # TODO: fill with actual samples and expected results

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part2(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 2: {sample_result} ----") # YOU MUST NOT change this output format

# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part2(lines)
print(f"---- Final result Part 2: {final_result} ----") # YOU MUST NOT change this output format
