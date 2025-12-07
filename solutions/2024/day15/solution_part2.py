# Edit this file: implement solve_part2

def solve_part2(lines):
    # Parse the map and moves
    map_lines = []
    moves = []
    parsing_moves = False
    
    for line in lines:
        if line.strip() == "":
            parsing_moves = True
            continue
        if parsing_moves:
            moves.extend(list(line.strip()))
        else:
            map_lines.append(line.strip())
    
    # Build the wide map (2x width)
    wide_map = []
    for row in map_lines:
        wide_row = ""
        for ch in row:
            if ch == "#":
                wide_row += "##"
            elif ch == "O":
                wide_row += "[]"
            elif ch == ".":
                wide_row += ".."
            elif ch == "@":
                wide_row += "@."
        wide_map.append(wide_row)
    
    # Find robot position
    robot_r, robot_c = -1, -1
    for r, row in enumerate(wide_map):
        for c, ch in enumerate(row):
            if ch == "@":
                robot_r, robot_c = r, c
                break
        if robot_r != -1:
            break
    
    # Process moves
    for move in moves:
        dr, dc = 0, 0
        if move == "^":
            dr = -1
        elif move == "v":
            dr = 1
        elif move == "<":
            dc = -1
        elif move == ">":
            dc = 1
        
        # Check what's in the way
        next_r, next_c = robot_r + dr, robot_c + dc
        if wide_map[next_r][next_c] == "#":
            # Wall - can't move
            continue
        
        if wide_map[next_r][next_c] == ".":
            # Empty space - move robot
            wide_map[robot_r] = wide_map[robot_r][:robot_c] + "." + wide_map[robot_r][robot_c+1:]
            wide_map[next_r] = wide_map[next_r][:next_c] + "@" + wide_map[next_r][next_c+1:]
            robot_r, robot_c = next_r, next_c
            continue
        
        if wide_map[next_r][next_c] in ["[", "]"]:
            # Box - need to check if it can be pushed
            if can_push_box(wide_map, next_r, next_c, dr, dc):
                push_box(wide_map, next_r, next_c, dr, dc)
                # Move robot
                wide_map[robot_r] = wide_map[robot_r][:robot_c] + "." + wide_map[robot_r][robot_c+1:]
                wide_map[next_r] = wide_map[next_r][:next_c] + "@" + wide_map[next_r][next_c+1:]
                robot_r, robot_c = next_r, next_c
    
    # Calculate GPS coordinates
    total_gps = 0
    for r, row in enumerate(wide_map):
        for c, ch in enumerate(row):
            if ch == "[":
                # This is the left half of a box
                total_gps += 100 * r + c
    
    return total_gps

def can_push_box(wide_map, r, c, dr, dc):
    """Check if a box at (r,c) can be pushed in direction (dr,dc)"""
    if wide_map[r][c] == "[":
        # Left half of box - check both halves
        if dc != 0:  # Horizontal push
            # Check if right half can move
            if not can_move_tile(wide_map, r, c+1, dr, dc):
                return False
        elif dr != 0:  # Vertical push
            # Check if both halves can move down/up
            if not can_move_tile(wide_map, r, c, dr, dc):
                return False
            if not can_move_tile(wide_map, r, c+1, dr, dc):
                return False
    elif wide_map[r][c] == "]":
        # Right half of box - check both halves
        if dc != 0:  # Horizontal push
            # Check if left half can move
            if not can_move_tile(wide_map, r, c-1, dr, dc):
                return False
        elif dr != 0:  # Vertical push
            # Check if both halves can move down/up
            if not can_move_tile(wide_map, r, c, dr, dc):
                return False
            if not can_move_tile(wide_map, r, c-1, dr, dc):
                return False
    
    return True

def can_move_tile(wide_map, r, c, dr, dc):
    """Check if a single tile can move"""
    new_r, new_c = r + dr, c + dc
    if new_r < 0 or new_r >= len(wide_map) or new_c < 0 or new_c >= len(wide_map[0]):
        return False
    if wide_map[new_r][new_c] == "#":
        return False
    if wide_map[new_r][new_c] in ["[", "]"]:
        # Recursively check if the box can be pushed
        return can_push_box(wide_map, new_r, new_c, dr, dc)
    return True

def push_box(wide_map, r, c, dr, dc):
    """Push a box at (r,c) in direction (dr,dc)"""
    if wide_map[r][c] == "[":
        if dc != 0:  # Horizontal push
            # Move right half
            new_r, new_c = r + dr, c + dc + 1
            wide_map[new_r] = wide_map[new_r][:new_c] + "]" + wide_map[new_r][new_c+1:]
            # Clear old position of right half
            wide_map[r] = wide_map[r][:c+1] + "." + wide_map[r][c+2:]
            
            # Move left half
            new_r, new_c = r + dr, c + dc
            wide_map[new_r] = wide_map[new_r][:new_c] + "[" + wide_map[new_r][new_c+1:]
            # Clear old position of left half
            wide_map[r] = wide_map[r][:c] + "." + wide_map[r][c+1:]
        elif dr != 0:  # Vertical push
            # Move both halves down/up
            for offset in [0, 1]:  # Left and right halves
                new_r, new_c = r + dr, c + offset
                wide_map[new_r] = wide_map[new_r][:new_c] + wide_map[r][c+offset] + wide_map[new_r][new_c+1:]
                wide_map[r] = wide_map[r][:c+offset] + "." + wide_map[r][c+offset+1:]
    elif wide_map[r][c] == "]":
        if dc != 0:  # Horizontal push
            # Move left half
            new_r, new_c = r + dr, c + dc - 1
            wide_map[new_r] = wide_map[new_r][:new_c] + "[" + wide_map[new_r][new_c+1:]
            # Clear old position of left half
            wide_map[r] = wide_map[r][:c-1] + "." + wide_map[r][c:]
            
            # Move right half
            new_r, new_c = r + dr, c + dc
            wide_map[new_r] = wide_map[new_r][:new_c] + "]" + wide_map[new_r][new_c+1:]
            # Clear old position of right half
            wide_map[r] = wide_map[r][:c] + "." + wide_map[r][c+1:]
        elif dr != 0:  # Vertical push
            # Move both halves down/up
            for offset in [-1, 0]:  # Left and right halves
                new_r, new_c = r + dr, c + offset
                wide_map[new_r] = wide_map[new_r][:new_c] + wide_map[r][c+offset] + wide_map[new_r][new_c+1:]
                wide_map[r] = wide_map[r][:c+offset] + "." + wide_map[r][c+offset+1:]

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples IF there are any samples given for part 2.
samples = [
    ("""########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<""", 2028),
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

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^<<>><>>v<vvv<>^v^>^<<<><<<v<<<v<^v>^<<>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<""", 9021)
]  # TODO: fill with actual samples and expected results

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

