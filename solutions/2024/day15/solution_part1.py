```python
# Edit this file: implement solve_part1

def solve_part1(lines):
    # Split input into warehouse map and moves
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
    robot_pos = None
    for r, row in enumerate(map_lines):
        for c, cell in enumerate(row):
            if cell == '@':
                robot_pos = (r, c)
                break
        if robot_pos:
            break
    
    # Convert map to list of lists for easier manipulation
    grid = [list(row) for row in map_lines]
    
    # Process moves
    dr = {'^': -1, 'v': 1, '<': 0, '>': 0}
    dc = {'^': 0, 'v': 0, '<': -1, '>': 1}
    
    for move in moves:
        r, c = robot_pos
        nr, nc = r + dr[move], c + dc[move]
        
        # Check what's in the target position
        target = grid[nr][nc]
        
        if target == '#':
            # Wall - can't move
            continue
        elif target == '.':
            # Empty - robot moves
            grid[r][c] = '.'
            grid[nr][nc] = '@'
            robot_pos = (nr, nc)
        elif target == 'O':
            # Box - need to check if it can be pushed
            # Find all consecutive boxes in this direction
            boxes_to_move = []
            current_r, current_c = nr, nc
            
            while True:
                boxes_to_move.append((current_r, current_c))
                next_r = current_r + dr[move]
                next_c = current_c + dc[move]
                
                if grid[next_r][next_c] == '#':
                    # Wall at the end - can't push
                    break
                elif grid[next_r][next_c] == '.':
                    # Empty space at the end - can push
                    # Move all boxes
                    for br, bc in boxes_to_move:
                        next_br = br + dr[move]
                        next_bc = bc + dc[move]
                        grid[next_br][next_bc] = 'O'
                        grid[br][bc] = '.'
                    
                    # Move robot
                    grid[r][c] = '.'
                    grid[nr][nc] = '@'
                    robot_pos = (nr, nc)
                    break
                elif grid[next_r][next_c] == 'O':
                    # Another box - continue checking
                    current_r, current_c = next_r, next_c
                else:
                    # Shouldn't happen
                    break
    
    # Calculate GPS coordinates sum
    total = 0
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == 'O':
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

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^<<>><>>v<vvv<>^v^>^<<<><<><v^<^^v>vv<^^v^<v^v^v<<<^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v^v<>vv>>><^<>>v>vvv^>vv<<v>^^>>^^^>><><v^<^^v>vv<^^v^<v^v^v<<<^^v<v>^<^^>v