from heapq import heappush, heappop
from collections import defaultdict

def solve_part2(lines):
    # Parse grid
    grid = [list(line) for line in lines]
    rows, cols = len(grid), len(grid[0])
    
    # Find start and end positions
    start = end = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'S':
                start = (r, c)
            elif grid[r][c] == 'E':
                end = (r, c)
    
    # Dijkstra to find shortest path distances
    # State: (row, col, direction)
    # Directions: 0=East, 1=South, 2=West, 3=North
    INF = float('inf')
    dist = defaultdict(lambda: INF)
    prev = defaultdict(list)  # state -> list of previous states
    
    # Priority queue: (cost, row, col, direction)
    pq = [(0, start[0], start[1], 0)]  # Start facing East
    dist[(start[0], start[1], 0)] = 0
    
    # Movement deltas for each direction
    dr = [0, 1, 0, -1]  # East, South, West, North
    dc = [1, 0, -1, 0]
    
    while pq:
        cost, r, c, d = heappop(pq)
        
        if cost > dist[(r, c, d)]:
            continue
            
        # Try moving forward
        nr, nc = r + dr[d], c + dc[d]
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#':
            new_cost = cost + 1
            if new_cost < dist[(nr, nc, d)]:
                dist[(nr, nc, d)] = new_cost
                prev[(nr, nc, d)] = [(r, c, d)]
                heappush(pq, (new_cost, nr, nc, d))
            elif new_cost == dist[(nr, nc, d)]:
                prev[(nr, nc, d)].append((r, c, d))
        
        # Try rotating clockwise and counterclockwise
        for nd in [(d + 1) % 4, (d - 1) % 4]:
            new_cost = cost + 1000
            if new_cost < dist[(r, c, nd)]:
                dist[(r, c, nd)] = new_cost
                prev[(r, c, nd)] = [(r, c, d)]
                heappush(pq, (new_cost, r, c, nd))
            elif new_cost == dist[(r, c, nd)]:
                prev[(r, c, nd)].append((r, c, d))
    
    # Find minimum distance to end position (any direction)
    min_dist = min(dist[(end[0], end[1], d)] for d in range(4))
    
    # Backtrack to find all tiles on any shortest path
    visited_tiles = set()
    
    def backtrack(state):
        if state in visited_tiles:
            return
        visited_tiles.add(state)
        
        r, c, d = state
        # Mark this tile as visited
        visited_tiles.add((r, c))
        
        # Continue backtracking
        for prev_state in prev[state]:
            backtrack(prev_state)
    
    # Start backtracking from all end states that have minimum distance
    for d in range(4):
        if dist[(end[0], end[1], d)] == min_dist:
            backtrack((end[0], end[1], d))
    
    return len(visited_tiles)

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples IF there are any samples given for part 2.
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
