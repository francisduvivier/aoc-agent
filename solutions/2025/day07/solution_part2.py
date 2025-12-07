def main():
    sample_input = [
        ".......S.......",
        "...............",
        ".......^.......",
        "...............",
        "......^.^......",
        "...............",
        ".....^.^.^.....",
        "...............",
        "....^.^...^....",
        "...............",
        "...^.^...^.^...",
        "...............",
        "..^...^.....^..",
        "...............",
        ".^.^.^.^.^...^.",
        "..............."
    ]
    sample_answer = 40

    with open('input.txt', 'r') as f:
        grid = [line.strip() for line in f.readlines()]

    def solve(g):
        rows, cols = len(g), len(g[0])
        start_col = next(i for i, ch in enumerate(g[0]) if ch == 'S')
        dp = [[0] * cols for _ in range(rows)]
        dp[0][start_col] = 1
        
        for r in range(rows):
            for c in range(cols):
                if dp[r][c] == 0:
                    continue
                if r + 1 < rows:
                    if g[r+1][c] == '.':
                        dp[r+1][c] += dp[r][c]
                    elif g[r+1][c] == '^':
                        if c - 1 >= 0:
                            dp[r+1][c-1] += dp[r][c]
                        if c + 1 < cols:
                            dp[r+1][c+1] += dp[r][c]
        return sum(dp[-1])

    sample_result = solve(sample_input)
    real_result = solve(grid)
    print(sample_result)
    print(real_result)

if __name__ == '__main__':
    main()
