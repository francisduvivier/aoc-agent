from functools import cache

def solve_part2(lines):
    stones = list(map(int, lines[0].split()))
    @cache
    def f(n, blinks):
        if blinks == 0:
            return 1
        s = str(n)
        if n == 0:
            return f(1, blinks - 1)
        if len(s) % 2 == 0:
            mid = len(s) // 2
            return f(int(s[:mid]), blinks - 1) + f(int(s[mid:]), blinks - 1)
        return f(n * 2024, blinks - 1)
    return sum(f(n, 75) for n in stones)

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples IF there are any samples given for part 2.
samples = []  # TODO: fill with actual samples and expected results

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part2(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 2: {sample_result} ----") # YOU MUST NOT change this output format
print(f"---- Sample NONE result Part 2: NONE ----") # Uncomment this if no samples are given for part 2
# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part2(lines)
print(f"---- Final result Part 2: {final_result} ----") # YOU MUST NOT change this output format

