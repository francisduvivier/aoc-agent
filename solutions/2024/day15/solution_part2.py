# Edit this file: implement solve_part2

def solve_part2(lines):
    # Find map lines and moves
    i = 0
    map_lines = []
    while i < len(lines) and lines[i] and lines[i][0] == '#':
        map_lines.append(lines[i])
        i += 1
    moves = ''.join(lines[i:]).replace('\n', '')
    
    # Scale the map for part 2
    new_map = []
    for line in map_lines:
        new_line = ''
        for ch in line:
            if ch == '#':
                new_line += '##'
            elif ch == 'O':
                new_line += '[]'
            elif ch == '.':
                new_line += '..'
            elif ch == '@':
                new_line += '@.'
        new_map.append(new_line)
    
    # Create grid
    grid = [list(row) for row in new_map]
    
    # Find robot position
    r, c = None, None
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '@':
                r, c = i, j
                break
        if r is not None:
            break
    
    # Directions
    dirs = {'<': (0, -1), '>': (0, 1), '^': (-1, 0), 'v': (1, 0)}
    
    # Simulate moves
    for move in moves:
        dr, dc = dirs[move]
        nr, nc = r + dr, c + dc
        if grid[nr][nc] == '#':
            continue
        if grid[nr][nc] == '.':
            grid[r][c] = '.'
            grid[nr][nc] = '@'
            r, c = nr, nc
            continue
        # Try to push
        if dc != 0:  # Horizontal
            if dc == 1:  # Right
                pos = c + 1
                if grid[r][pos] == '.':
                    grid[r][c] = '.'
                    grid[r][pos] = '@'
                    r, c = r, pos
                elif grid[r][pos] == '#':
                    continue
                else:
                    end_pos = pos
                    while end_pos < len(grid[0]) and grid[r][end_pos] in '[]':
                        end_pos += 2
                    if end_pos >= len(grid[0]) or grid[r][end_pos] == '#':
                        continue
                    for p in range(end_pos, pos, -1):
                        grid[r][p] = grid[r][p-1]
                    grid[r][pos] = '.'
                    grid[r][c] = '.'
                    grid[r][c+1] = '@'
                    r, c = r, c+1
            else:  # Left
                pos = c - 1
                if grid[r][pos] == '.':
                    grid[r][c] = '.'
                    grid[r][pos] = '@'
                    r, c = r, pos
                elif grid[r][pos] == '#':
                    continue
                else:
                    end_pos = pos
                    while end_pos >= 0 and grid[r][end_pos] in '[]':
                        end_pos -= 2
                    if end_pos < 0 or grid[r][end_pos] == '#':
                        continue
                    for p in range(end_pos, pos):
                        grid[r][p] = grid[r][p+1]
                    grid[r][pos] = '.'
                    grid[r][c] = '.'
                    grid[r][c-1] = '@'
                    r, c = r, c-1
        else:  # Vertical
            from collections import deque
            to_move = set()
            q = deque()
            if grid[nr][nc] == '[':
                box = (nr, nc)
            else:
                box = (nr, nc-1)
            q.append(box)
            to_move.add(box)
            can_move = True
            while q and can_move:
                br, bc = q.popleft()
                new_r = br + dr
                for cc in [bc, bc+1]:
                    if grid[new_r][cc] == '#':
                        can_move = False
                        break
                    elif grid[new_r][cc] == '[':
                        new_box = (new_r, cc)
                        if new_box not in to_move:
                            to_move.add(new_box)
                            q.append(new_box)
                    elif grid[new_r][cc] == ']':
                        new_box = (new_r, cc-1)
                        if new_box not in to_move:
                            to_move.add(new_box)
                            q.append(new_box)
            if not can_move:
                continue
            # Move boxes
            for br, bc in to_move:
                grid[br][bc] = '.'
                grid[br][bc+1] = '.'
            for br, bc in to_move:
                new_r = br + dr
                grid[new_r][bc] = '['
                grid[new_r][bc+1] = ']'
            # Move robot
            grid[r][c] = '.'
            grid[nr][nc] = '@'
            r, c = nr, nc
    
    # Calculate GPS sum
    total = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '[':
                total += 100 * i + j
    return total

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples IF there are any samples given for part 2.
samples = [("""##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<<>><>v<vvv<>^v^>^<<<><<<v<<<v^vv^v>vvv<><>vv<<<^^>>>>v<>^>^v<v^vv^v^<^>vvv>v>^^v^v<>vv>>><^<>v>vvv>vv<<v>^^>>^^^><>v^<^^v>vv<^^v< v^v^v<<<^^v<v>^<""", 9021)]  # TODO: fill with actual samples and expected results

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
