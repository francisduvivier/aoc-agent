# Edit this file: implement solve_part2

def solve_part2(lines):
    # Parse the map and moves
    map_lines = []
    moves = []
    parsing_map = True
    
    for line in lines:
        if line.strip() == "":
            parsing_map = False
            continue
        if parsing_map:
            map_lines.append(line)
        else:
            moves.extend(list(line))
    
    # Expand the map: # -> ##, O -> [], . -> .., @ -> @.
    expanded_map = []
    robot_pos = None
    for r, row in enumerate(map_lines):
        new_row = []
        for c, ch in enumerate(row):
            if ch == '#':
                new_row.extend(['#', '#'])
            elif ch == 'O':
                new_row.extend(['[', ']'])
            elif ch == '.':
                new_row.extend(['.', '.'])
            elif ch == '@':
                new_row.extend(['@', '.'])
                robot_pos = (r, c * 2)
            else:
                new_row.extend([ch, ch])
        expanded_map.append(new_row)
    
    # Helper to check if a position is within bounds and not a wall
    def is_valid(r, c):
        return 0 <= r < len(expanded_map) and 0 <= c < len(expanded_map[0]) and expanded_map[r][c] != '#'
    
    # Helper to check if a push is possible in a given direction
    # Returns True if all boxes that would be moved can be moved
    def can_push(r, c, dr, dc):
        # BFS to find all tiles that would move
        from collections import deque
        q = deque([(r, c)])
        tiles_to_move = set()
        visited = set()
        
        while q:
            cr, cc = q.popleft()
            if (cr, cc) in visited:
                continue
            visited.add((cr, cc))
            tiles_to_move.add((cr, cc))
            
            # Determine the type of tile and its neighbors to check
            if expanded_map[cr][cc] == '[':
                # Left half of a box: check right neighbor and both halves in direction
                neighbors = [(cr, cc + 1), (cr + dr, cc + dc), (cr + dr, cc + 1 + dc)]
            elif expanded_map[cr][cc] == ']':
                # Right half of a box: check left neighbor and both halves in direction
                neighbors = [(cr, cc - 1), (cr + dr, cc + dc), (cr + dr, cc - 1 + dc)]
            else:
                # Should not happen for boxes
                continue
            
            for nr, nc in neighbors:
                if not is_valid(nr, nc) and expanded_map[nr][nc] not in '[]':
                    # Wall or empty, no need to check further
                    continue
                if expanded_map[nr][nc] in '[]' and (nr, nc) not in visited:
                    q.append((nr, nc))
        
        # Check if any tile in the direction of movement is a wall
        for tr, tc in tiles_to_move:
            nr, nc = tr + dr, tc + dc
            if not (0 <= nr < len(expanded_map) and 0 <= nc < len(expanded_map[0])):
                return False
            if expanded_map[nr][nc] == '#':
                return False
        
        return True
    
    # Helper to actually move the boxes
    def move_boxes(r, c, dr, dc):
        from collections import deque
        q = deque([(r, c)])
        tiles_to_move = set()
        visited = set()
        
        while q:
            cr, cc = q.popleft()
            if (cr, cc) in visited:
                continue
            visited.add((cr, cc))
            tiles_to_move.add((cr, cc))
            
            if expanded_map[cr][cc] == '[':
                neighbors = [(cr, cc + 1), (cr + dr, cc + dc), (cr + dr, cc + 1 + dc)]
            elif expanded_map[cr][cc] == ']':
                neighbors = [(cr, cc - 1), (cr + dr, cc + dc), (cr + dr, cc - 1 + dc)]
            else:
                continue
            
            for nr, nc in neighbors:
                if expanded_map[nr][nc] in '[]' and (nr, nc) not in visited:
                    q.append((nr, nc))
        
        # Move tiles
        for tr, tc in sorted(tiles_to_move, reverse=(dr > 0 or dc > 0)):
            nr, nc = tr + dr, tc + dc
            expanded_map[nr][nc] = expanded_map[tr][tc]
            expanded_map[tr][tc] = '.'
    
    # Process moves
    dir_map = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}
    
    for move in moves:
        dr, dc = dir_map[move]
        r, c = robot_pos
        nr, nc = r + dr, c + dc
        
        if not is_valid(nr, nc):
            continue
        
        # Check what's in the direction of movement
        target = expanded_map[nr][nc]
        if target == '.':
            # Move robot
            expanded_map[r][c] = '.'
            expanded_map[nr][nc] = '@'
            robot_pos = (nr, nc)
        elif target in '[]':
            # Try to push
            if can_push(nr, nc, dr, dc):
                move_boxes(nr, nc, dr, dc)
                # Move robot
                expanded_map[r][c] = '.'
                expanded_map[nr][nc] = '@'
                robot_pos = (nr, nc)
    
    # Calculate GPS sum
    gps_sum = 0
    for r in range(len(expanded_map)):
        for c in range(len(expanded_map[0])):
            if expanded_map[r][c] == '[':
                # Left edge of a box
                gps_sum += 100 * r + c
    
    return gps_sum

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

<^^>>>vv<v>v<v<""",
2028),
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

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<^v^><<<<><<v<<<v^vv^v>^
vvv<^>^v^^<<>>>^<<^<^vv^^<vvv>><^^v>^>vv<v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>>>^<^^>vv>v<<<^^>vv^<^^>v^^<^^v>^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<^>^^>^^^vv<><v<>v<^^vv<^^<^^vv<^^<^v>>^^^^<^>^>vvv<
^>^v><^>^<^v<>><>v<>v<>^v<^vvv<>^<><><^<v^^vv^<v<^^<>v^^^v<^><<><>^>v><^v<>v<
^>><^>v<^><<v<v<><><v<^vvv><^<><><^<v^vv><^><v><>v<>><v^vv<>v<^><v<>><v^vvv<
<^<^>^^>^^>v<>^<v^>v<>^<^^v<>><v<^^><>^v<^^>>^^><v^vvvv<>v<^^><><v<>^<v^v<>>
^>><<><>^vv^^><vv<><>v><<^vv<>v<^><>>^><^<>^^<vv^vv^<><>>^<^v^vvv<>^<<>^v^>v
><^>vv>^<^<>^<v>v<>vvv>^<^<^vv>^v>^<^>v><^>^<>^<v><v<v<>vvv>^<^<><^^>^<^v<>vv<
><<^>^^^<><vvvv>^<^<v<>^><v><v<<>^^<^^<^^><^^><^><^><^^>^^<^^<v><><><>^>^<v<>>
^^>vv<^v^v<vv>^<><<>^>^v^><<<^^v^>^^^><^^<>^<><^v>v><^^>^<><><^v><^^>>^vvv<^
""",
9021)
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

