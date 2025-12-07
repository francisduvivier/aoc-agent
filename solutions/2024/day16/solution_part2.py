import heapq
from collections import defaultdict

def solve_part2(lines):
    # Parse the maze
    maze = [list(line) for line in lines]
    rows, cols = len(maze), len(maze[0])
    
    # Find start and end positions
    start = end = None
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == 'S':
                start = (r, c)
            elif maze[r][c] == 'E':
                end = (r, c)
    
    # Dijkstra's algorithm to find shortest path cost
    # State: (cost, row, col, direction)
    # Directions: 0=East, 1=South, 2=West, 3=North
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    # Priority queue for Dijkstra
    pq = [(0, start[0], start[1], 0)]  # Start facing East
    
    # Distance array: dist[r][c][dir] = minimum cost to reach (r,c) facing dir
    INF = float('inf')
    dist = [[[INF] * 4 for _ in range(cols)] for _ in range(rows)]
    dist[start[0]][start[1]][0] = 0
    
    # Track predecessors for path reconstruction
    prev = {}  # key: (r, c, dir), value: (prev_r, prev_c, prev_dir, move_type)
    
    while pq:
        cost, r, c, dir_idx = heapq.heappop(pq)
        
        if cost > dist[r][c][dir_idx]:
            continue
            
        # If we reached the end, we can stop
        if (r, c) == end:
            break
            
        # Try moving forward
        dr, dc = directions[dir_idx]
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != '#':
            new_cost = cost + 1
            if new_cost < dist[nr][nc][dir_idx]:
                dist[nr][nc][dir_idx] = new_cost
                prev[(nr, nc, dir_idx)] = (r, c, dir_idx, 'forward')
                heapq.heappush(pq, (new_cost, nr, nc, dir_idx))
        
        # Try rotating clockwise
        new_dir = (dir_idx + 1) % 4
        new_cost = cost + 1000
        if new_cost < dist[r][c][new_dir]:
            dist[r][c][new_dir] = new_cost
            prev[(r, c, new_dir)] = (r, c, dir_idx, 'rotate_cw')
            heapq.heappush(pq, (new_cost, r, c, new_dir))
        
        # Try rotating counterclockwise
        new_dir = (dir_idx - 1) % 4
        new_cost = cost + 1000
        if new_cost < dist[r][c][new_dir]:
            dist[r][c][new_dir] = new_cost
            prev[(r, c, new_dir)] = (r, c, dir_idx, 'rotate_ccw')
            heapq.heappush(pq, (new_cost, r, c, new_dir))
    
    # Find the minimum cost to reach the end
    min_cost = min(dist[end[0]][end[1]])
    
    # Collect all tiles that are part of any optimal path
    # Use BFS from the end to find all reachable states with optimal cost
    visited_states = set()
    queue = []
    
    # Start from all end states that have the minimum cost
    for dir_idx in range(4):
        if dist[end[0]][end[1]][dir_idx] == min_cost:
            queue.append((end[0], end[1], dir_idx))
            visited_states.add((end[0], end[1], dir_idx))
    
    # Track all visited positions (regardless of direction)
    visited_positions = set()
    for r, c, _ in queue:
        visited_positions.add((r, c))
    
    # Work backwards to find all states that can reach the end with optimal cost
    while queue:
        r, c, dir_idx = queue.pop(0)
        
        # Check all possible previous states
        # 1. Came from forward move
        dr, dc = directions[dir_idx]
        pr, pc = r - dr, c - dc
        if 0 <= pr < rows and 0 <= pc < cols and maze[pr][pc] != '#':
            if dist[pr][pc][dir_idx] + 1 == dist[r][c][dir_idx]:
                if (pr, pc, dir_idx) not in visited_states:
                    visited_states.add((pr, pc, dir_idx))
                    visited_positions.add((pr, pc))
                    queue.append((pr, pc, dir_idx))
        
        # 2. Rotated from clockwise
        prev_dir = (dir_idx - 1) % 4
        if dist[r][c][prev_dir] + 1000 == dist[r][c][dir_idx]:
            if (r, c, prev_dir) not in visited_states:
                visited_states.add((r, c, prev_dir))
                visited_positions.add((r, c))
                queue.append((r, c, prev_dir))
        
        # 3. Rotated from counterclockwise
        prev_dir = (dir_idx + 1) % 4
        if dist[r][c][prev_dir] + 1000 == dist[r][c][dir_idx]:
            if (r, c, prev_dir) not in visited_states:
                visited_states.add((r, c, prev_dir))
                visited_positions.add((r, c))
                queue.append((r, c, prev_dir))
    
    return len(visited_positions)

# Sample data
samples = [
("""###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############""", 45),
("""#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################""", 64)
]

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part2(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 2: {sample_result} ----")
# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part2(lines)
print(f"---- Final result Part 2: {final_result} ----")
