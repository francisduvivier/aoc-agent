def solve_part2(lines):
    # Separate map lines and move lines
    map_lines = []
    move_lines = []
    is_map = True
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if is_map and all(c in '#.O@ ' for c in stripped):
            map_lines.append(stripped)
        else:
            is_map = False
            move_lines.append(stripped)
    moves = ''.join(move_lines).strip()

    # Scale the map
    scaled_map = []
    for line in map_lines:
        scaled_line = []
        for c in line:
            if c == '#':
                scaled_line.append('##')
            elif c == 'O':
                scaled_line.append('[]')
            elif c == '.':
                scaled_line.append('..')
            elif c == '@':
                scaled_line.append('@.')
            else:
                scaled_line.append('  ')  # for spaces or others
        scaled_map.append(''.join(scaled_line))

    # Find robot's initial position
    robot_pos = None
    for i, row in enumerate(scaled_map):
        for j, c in enumerate(row):
            if c == '@':
                robot_pos = (i, j)
                break
        if robot_pos is not None:
            break
    if robot_pos is None:
        return 0  # no robot found

    # Convert to list of lists for mutability
    scaled_map = [list(row) for row in scaled_map]
    height = len(scaled_map)
    width = len(scaled_map[0]) if height > 0 else 0

    directions = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}

    for move in moves:
        dr, dc = directions[move]
        r, c = robot_pos
        new_r = r + dr
        new_c = c + dc

        if not (0 <= new_r < height and 0 <= new_c < width):
            continue

        target_char = scaled_map[new_r][new_c]

        if target_char == '.':
            scaled_map[r][c] = '.'
            scaled_map[new_r][new_c] = '@'
            robot_pos = (new_r, new_c)
        elif target_char == '#':
            continue
        elif target_char in ['[', ']']:
            # Determine the box's left and right positions
            if target_char == '[':
                box_r = new_r
                box_c1 = new_c
                box_c2 = new_c + 1
            else:  # target_char == ']'
                box_r = new_r
                box_c1 = new_c - 1
                box_c2 = new_c

            # Check if box_c2 is valid and part of the box
            if box_c2 >= width or scaled_map[box_r][box_c2] != ']':
                continue

            # Calculate new box positions
            new_box_r = box_r + dr
            new_box_c1 = box_c1 + dc
            new_box_c2 = box_c2 + dc

            # Check if new positions are within bounds and empty
            if (0 <= new_box_r < height and 
                0 <= new_box_c1 < width and 
                0 <= new_box_c2 < width and 
                scaled_map[new_box_r][new_box_c1] == '.' and 
                scaled_map[new_box_r][new_box_c2] == '.'):
                
                # Move the box
                scaled_map[box_r][box_c1] = '.'
                scaled_map[box_r][box_c2] = '.'
                scaled_map[new_box_r][new_box_c1] = '['
                scaled_map[new_box_r][new_box_c2] = ']'
                
                # Move the robot
                scaled_map[r][c] = '.'
                scaled_map[new_r][new_c] = '@'
                robot_pos = (new_r, new_c)

    # Calculate the sum of GPS coordinates for all boxes
    total = 0
    for i, row in enumerate(scaled_map):
        for j, c in enumerate(row):
            if c == '[':
                total += 100 * i + j
    return total

# Sample data
samples = []
# Sample from the problem statement (scaled larger example)
sample_input = """
####################
##....[]....[]..[]##
##............[]..##
##..[][]....[]..[]##
##....[]@.....[]..##
##[]##....[]......##
##[]....[]....[]..##
##..[][]..[]..[][]##
##........[]......##
####################
<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
""".strip()
expected_result = 9021
samples.append((sample_input, expected_result))

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part2(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 2: {sample_result} ----")

# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part2(lines)
print(f"---- Final result Part 2: {final_result} ----")
