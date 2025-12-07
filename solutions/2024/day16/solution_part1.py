# Edit this file: implement solve_part1

def solve_part1(lines):
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
    
    # Directions: 0=East, 1=South, 2=West, 3=North
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    # Dijkstra's algorithm
    import heapq
    # State: (cost, row, col, direction)
    pq = [(0, start[0], start[1], 0)]  # Start facing East
    # Best cost for (row, col, direction)
    best = {}
    
    while pq:
        cost, r, c, d = heapq.heappop(pq)
        
        # If we reached the end, return the cost
        if (r, c) == end:
            return cost
        
        # Skip if we've seen this state with lower cost
        if (r, c, d) in best and best[(r, c, d)] <= cost:
            continue
        best[(r, c, d)] = cost
        
        # Try moving forward
        dr, dc = dirs[d]
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != '#':
            heapq.heappush(pq, (cost + 1, nr, nc, d))
        
        # Try turning left and right
        for nd in [(d + 1) % 4, (d - 1) % 4]:
            heapq.heappush(pq, (cost + 1000, r, c, nd))
    
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
###############""".splitlines(), 7036),
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
#################""".splitlines(), 11048)
]  # TODO: fill with actual samples and expected results

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part1(sample_input)
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 1: {sample_result} ----") # YOU MUST NOT change this output format

# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part1(lines)
print(f"---- Final result Part 1: {final_result} ----") # YOU MUST NOT change this output format

