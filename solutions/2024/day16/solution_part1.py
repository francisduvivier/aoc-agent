from heapq import heappush, heappop

def solve_part1(lines):
    # Parse grid
    grid = [list(line) for line in lines]
    rows, cols = len(grid), len(grid[0])
    
    # Find start (S) and end (E)
    start = end = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'S':
                start = (r, c)
            elif grid[r][c] == 'E':
                end = (r, c)
    
    # Directions: 0=East, 1=South, 2=West, 3=North
    dr = [0, 1, 0, -1]
    dc = [1, 0, -1, 0]
    
    # Dijkstra's algorithm
    # State: (cost, row, col, direction)
    pq = [(0, start[0], start[1], 0)]  # Start facing East
    # visited[r][c][dir] = best cost to reach (r,c) facing dir
    visited = [[[float('inf')] * 4 for _ in range(cols)] for _ in range(rows)]
    visited[start[0]][start[1]][0] = 0
    
    while pq:
        cost, r, c, d = heappop(pq)
        
        if (r, c) == end:
            return cost
            
        if cost > visited[r][c][d]:
            continue
            
        # Try moving forward
        nr, nc = r + dr[d], c + dc[d]
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#':
            new_cost = cost + 1
            if new_cost < visited[nr][nc][d]:
                visited[nr][nc][d] = new_cost
                heappush(pq, (new_cost, nr, nc, d))
        
        # Try rotating clockwise and counterclockwise
        for nd in [(d + 1) % 4, (d - 1) % 4]:
            new_cost = cost + 1000
            if new_cost < visited[r][c][nd]:
                visited[r][c][nd] = new_cost
                heappush(pq, (new_cost, r, c, nd))
    
    return -1  # No path found

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples.
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
###############""", 7036),
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
#################""", 11048)
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
