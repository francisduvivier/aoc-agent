# Edit this file: implement solve_part1

def solve_part1(lines):
    # Parse the grid and moves
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
    
    # Find robot position and create grid
    grid = [list(row) for row in grid_lines]
    rows, cols = len(grid), len(grid[0])
    
    robot_r, robot_c = -1, -1
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '@':
                robot_r, robot_c = r, c
                break
        if robot_r != -1:
            break
    
    # Process moves
    for move in moves:
        dr, dc = 0, 0
        if move == '^':
            dr = -1
        elif move == 'v':
            dr = 1
        elif move == '<':
            dc = -1
        elif move == '>':
            dc = 1
        
        # Check what's in the way
        nr, nc = robot_r + dr, robot_c + dc
        
        if grid[nr][nc] == '#':
            # Wall - can't move
            continue
        
        if grid[nr][nc] == '.':
            # Empty space - move robot
            grid[robot_r][robot_c] = '.'
            grid[nr][nc] = '@'
            robot_r, robot_c = nr, nc
            continue
        
        if grid[nr][nc] == 'O':
            # Box - need to check if we can push it
            # Find how many consecutive boxes are in this direction
            boxes_to_move = []
            r, c = nr, nc
            
            while grid[r][c] == 'O':
                boxes_to_move.append((r, c))
                r += dr
                c += dc
                
                # Check if we hit a wall or go out of bounds
                if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == '#':
                    boxes_to_move = []  # Can't push
                    break
            
            if boxes_to_move:
                # Move all boxes
                for r_box, c_box in reversed(boxes_to_move):
                    grid[r_box + dr][c_box + dc] = 'O'
                    grid[r_box][c_box] = '.'
                
                # Move robot
                grid[robot_r][robot_c] = '.'
                grid[nr][nc] = '@'
                robot_r, robot_c = nr, nc
    
    # Calculate GPS coordinates sum
    gps_sum = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'O':
                gps_sum += 100 * r + c
    
    return gps_sum

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples.
samples = [
    ("""########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>v<v<""", 2028),
    ("""##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^<<>><>>v<vvv<>^v^>^<<<><<v<<<v<^v>^<<>>v<v<v^^>vv>vvv<><>vv<<<^^>>>>v<>^>^v<v^vv^v^<^>vvv>v>^^v^v<>vv>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<""", 10092)
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

