def solve_part2(lines):
    grid = [list(line) for line in lines]
    rows, cols = len(grid), len(grid[0])
    
    # Find starting position
    start_col = None
    for j in range(cols):
        if grid[0][j] == 'S':
            start_col = j
            break
    
    if start_col is None:
        return 0
    
    # DP: dp[i][j] = number of timelines at position (i, j)
    dp = [[0] * cols for _ in range(rows)]
    dp[0][start_col] = 1
    
    for i in range(rows - 1):
        for j in range(cols):
            if dp[i][j] == 0:
                continue
            
            if grid[i][j] == '^':
                # Split to left and right
                if j > 0:
                    dp[i+1][j-1] += dp[i][j]
                if j < cols - 1:
                    dp[i+1][j+1] += dp[i][j]
            else:
                # Continue downward
                dp[i+1][j] += dp[i][j]
    
    return sum(dp[-1])

if __name__ == '__main__':
    sample_input = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""
    sample_answer = 40

    # Test run
    print(solve_part2(sample_input.strip().splitlines()))

    with open('input.txt') as f:
        lines = [line.strip() for line in f]
    print(solve_part2(lines))
