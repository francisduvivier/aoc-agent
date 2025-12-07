# Edit this file: implement solve_part1

def solve_part1(lines):
    # Parse the input: split into grid and moves
    grid_lines = []
    moves = []
    parsing_moves = False
    
    for line in lines:
        if line.strip() == "":
            parsing_moves = True
            continue
        if parsing_moves:
            moves.extend(list(line.strip()))
        else:
            grid_lines.append(line.strip())
    
    # Build the grid as a list of lists for mutability
    grid = [list(row) for row in grid_lines]
    
    # Find the robot position
    robot_r, robot_c = None, None
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == '@':
                robot_r, robot_c = r, c
                break
        if robot_r is not None:
            break
    
    # Define movement deltas
    delta = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}
    
    # Process each move
    for move in moves:
        dr, dc = delta[move]
        nr, nc = robot_r + dr, robot_c + dc
        
        # If the next cell is a wall, nothing moves
        if grid[nr][nc] == '#':
            continue
        
        # If the next cell is empty, just move the robot
        if grid[nr][nc] == '.':
            grid[robot_r][robot_c] = '.'
            grid[nr][nc] = '@'
            robot_r, robot_c = nr, nc
            continue
        
        # If the next cell is a box, attempt to push it
        if grid[nr][nc] == 'O':
            # Find the farthest box in the line of push
            push_path = []
            pr, pc = robot_r, robot_c
            while True:
                pr += dr
                pc += dc
                if grid[pr][pc] == '#':
                    # Blocked by wall, nothing moves
                    break
                push_path.append((pr, pc))
                if grid[pr][pc] == '.':
                    # Found empty space, can push
                    # Move boxes backward along the path
                    for i in range(len(push_path) - 1, 0, -1):
                        r1, c1 = push_path[i]
                        r2, c2 = push_path[i - 1]
                        grid[r1][c1] = grid[r2][c2]
                    # Move the robot
                    grid[robot_r][robot_c] = '.'
                    grid[robot_r + dr][robot_c + dc] = '@'
                    robot_r, robot_c = robot_r + dr, robot_c + dc
                    break
                if grid[pr][pc] == '#':
                    # Blocked, break without moving
                    break
    
    # Calculate GPS coordinates sum
    total = 0
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == 'O':
                total += 100 * r + c
    
    return total

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples.
samples = [
    (
        """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<""",
        2028
    ),
    (
        """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^<<>><>>v<vvv<>^v^>^<<<><<<>v<vvv><>^<v<>^v<v^vv^v<^>vvv>v>^^v^v<>vv>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<""",
        10092
    )
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

