def solve_part2(lines):
    # Parse input into map and moves
    map_lines = []
    moves_lines = []
    is_map = True
    for line in lines:
        stripped = line.strip()
        if not stripped:
            is_map = False
            continue
        if is_map and any(c in stripped for c in '#.O@'):
            map_lines.append(stripped)
        else:
            is_map = False
            moves_lines.append(stripped)
    moves = ''.join(moves_lines).replace('\n', '')

    # Transform the map
    transformed = []
    for line in map_lines:
        new_line = []
        for c in line:
            if c == '#':
                new_line.append('##')
            elif c == 'O':
                new_line.append('[]')
            elif c == '.':
                new_line.append('..')
            elif c == '@':
                new_line.append('@.')
            else:
                new_line.append('  ')  # should not happen
        transformed.append(''.join(new_line))
    
    # Parse the transformed map into grid, robot, and boxes
    grid = []
    robot = None
    boxes = set()
    for y, row in enumerate(transformed):
        grid_row = list(row)
        grid.append(grid_row)
        x = 0
        while x < len(grid_row):
            c = grid_row[x]
            if c == '@':
                if robot is None:
                    robot = (x, y)
                x += 1  # skip the next '.' as it's part of robot
            elif c == '[':
                if x + 1 < len(grid_row) and grid_row[x+1] == ']':
                    boxes.add((x, y))
                    x += 1  # skip the ']'
            x += 1

    # Define helper function to get push chain
    def get_push_chain(box_x, box_y, dx, dy, grid, boxes, visited):
        if (box_x, box_y) in visited:
            return None
        visited.add((box_x, box_y))
        
        width = len(grid[0])
        height = len(grid)
        
        if dx != 0:
            if dx == 1:
                check_x = box_x + 2
                check_y = box_y
            else:
                check_x = box_x - 1
                check_y = box_y
            cells_to_check = [(check_x, check_y)]
        else:
            if dy == -1:
                check_y = box_y - 1
            else:
                check_y = box_y + 1
            cells_to_check = [(box_x, check_y), (box_x + 1, check_y)]
        
        chain = [(box_x, box_y)]
        for (cx, cy) in cells_to_check:
            if cx < 0 or cx >= width or cy < 0 or cy >= height:
                return None
            cell = grid[cy][cx]
            if cell == '#':
                return None
            elif cell == '[' or cell == ']':
                if cell == ']':
                    left_x = cx - 1
                else:
                    left_x = cx
                if (left_x, cy) not in boxes:
                    return None
                sub_chain = get_push_chain(left_x, cy, dx, dy, grid, boxes, visited)
                if sub_chain is None:
                    return None
                chain.extend(sub_chain)
        return chain

    # Process each move
    directions = {'>': (1, 0), '<': (-1, 0), '^': (0, -1), 'v': (0, 1)}
    rx, ry = robot
    for move in moves:
        dx, dy = directions[move]
        new_rx = rx + dx
        new_ry = ry + dy
        
        if new_ry < 0 or new_ry >= len(grid) or new_rx < 0 or new_rx >= len(grid[0]):
            continue
        
        cell = grid[new_ry][new_rx]
        if cell == '#':
            continue
        elif cell == '.' or cell == '@':
            grid[ry][rx] = '.'
            grid[new_ry][new_rx] = '@'
            rx, ry = new_rx, new_ry
        elif cell == '[' or cell == ']':
            if cell == '[':
                box_x, box_y = new_rx, new_ry
            else:
                box_x, box_y = new_rx - 1, new_ry
            
            if (box_x, box_y) not in boxes:
                continue
            
            visited = set()
            chain = get_push_chain(box_x, box_y, dx, dy, grid, boxes, visited)
            if chain is None:
                continue
            
            # Push boxes in reverse order
            for (bx, by) in reversed(chain):
                if (bx, by) not in boxes:
                    continue  # Safety check to avoid KeyError
                boxes.remove((bx, by))
                grid[by][bx] = '.'
                grid[by][bx + 1] = '.'
                new_bx = bx + dx
                new_by = by + dy
                boxes.add((new_bx, new_by))
                grid[new_by][new_bx] = '['
                grid[new_by][new_bx + 1] = ']'
            
            # Move robot
            grid[ry][rx] = '.'
            grid[new_ry][new_rx] = '@'
            rx, ry = new_rx, new_ry
    
    # Calculate GPS sum
    total = 0
    for (x, y) in boxes:
        total += 100 * y + x
    return total

samples = []  # No samples provided for part 2 in the problem statement

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part2(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 2: {sample_result} ----")

print("---- Sample NONE result Part 2: NONE ----")

with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part2(lines)
print(f"---- Final result Part 2: {final_result} ----")
