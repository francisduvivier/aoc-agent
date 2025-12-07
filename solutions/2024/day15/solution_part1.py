# Edit this file: implement solve_part1

def solve_part1(lines):
    # Split into map and moves
    map_lines = []
    moves = []
    reading_moves = False
    
    for line in lines:
        if line.strip() == "":
            reading_moves = True
            continue
        if reading_moves:
            moves.extend(list(line.strip()))
        else:
            map_lines.append(line.strip())
    
    # Find robot position
    robot_r, robot_c = None, None
    for r, row in enumerate(map_lines):
        for c, ch in enumerate(row):
            if ch == '@':
                robot_r, robot_c = r, c
                break
        if robot_r is not None:
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
        if map_lines[nr][nc] == '#':
            # Wall - can't move
            continue
        
        # Find boxes to push
        boxes_to_move = []
        r, c = nr, nc
        while 0 <= r < len(map_lines) and 0 <= c < len(map_lines[0]):
            if map_lines[r][c] == '#':
                # Hit a wall - can't move anything
                boxes_to_move = None
                break
            elif map_lines[r][c] == 'O':
                boxes_to_move.append((r, c))
                r += dr
                c += dc
            else:
                # Empty space or robot - stop
                break
        
        if boxes_to_move is None:
            # Can't move due to wall
            continue
        
        # Move boxes
        for r, c in reversed(boxes_to_move):
            # Convert box to empty
            map_lines[r] = map_lines[r][:c] + '.' + map_lines[r][c+1:]
            # Move box forward
            map_lines[r + dr] = map_lines[r + dr][:c + dc] + 'O' + map_lines[r + dr][c + dc + 1:]
        
        # Move robot
        map_lines[robot_r] = map_lines[robot_r][:robot_c] + '.' + map_lines[robot_r][robot_c+1:]
        robot_r, robot_c = nr, nc
        map_lines[robot_r] = map_lines[robot_r][:robot_c] + '@' + map_lines[robot_r][robot_c+1:]
    
    # Calculate GPS coordinates
    total = 0
    for r, row in enumerate(map_lines):
        for c, ch in enumerate(row):
            if ch == 'O':
                total += 100 * r + c
    
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

<^^>>>vv<v>>v<<""", 2028)
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

