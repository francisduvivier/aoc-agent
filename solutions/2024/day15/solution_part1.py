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
    robot_pos = None
    grid = []
    for r, row in enumerate(grid_lines):
        grid_row = []
        for c, ch in enumerate(row):
            if ch == '@':
                robot_pos = (r, c)
                grid_row.append('.')
            else:
                grid_row.append(ch)
        grid.append(grid_row)
    
    # Process moves
    r, c = robot_pos
    for move in moves:
        dr, dc = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}[move]
        nr, nc = r + dr, c + dc
        
        # Check what's in the way
        if grid[nr][nc] == '#':
            # Wall - don't move
            continue
        elif grid[nr][nc] == '.':
            # Empty - move robot
            r, c = nr, nc
        else:  # grid[nr][nc] == 'O'
            # Box - try to push it
            # Find how far the box chain extends
            push_chain = []
            pr, pc = nr, nc
            while grid[pr][pc] == 'O':
                push_chain.append((pr, pc))
                pr, pc = pr + dr, pc + dc
            
            # Check if we can push the chain
            if grid[pr][pc] == '#':
                # Can't push - don't move
                continue
            else:
                # Can push - move the chain and robot
                for pr, pc in reversed(push_chain):
                    grid[pr + dr][pc + dc] = 'O'
                    grid[pr][pc] = '.'
                r, c = nr, nc
    
    # Calculate GPS coordinates
    total = 0
    for r_idx, row in enumerate(grid):
        for c_idx, ch in enumerate(row):
            if ch == 'O':
                total += 100 * r_idx + c_idx
    
    return total

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

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^<<>><>>v<vvv<>^v^>^<<<><<><v^<^^v><<^v<<>>v<v<v^^>vv>vvv<><>vv<<<^^>>>>v<>^>^v<v^vv^v^<^>vvv>v>^^v^v<>vv>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<

vvv<<^>^v^^<<>>>><^<<><^vv^^<>>vvv>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>>>><>><>^<<^^>vv>v<<^^^>>v^v^<^^>v^^>v^<^v>vv>vvv><^^v>^>vv<<^>v^^>vv<^^v^<v<^v>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<""", 10092)
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

