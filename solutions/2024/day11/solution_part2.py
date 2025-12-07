from functools import cache

def solve_part2(lines):
    stones = list(map(int, lines[0].split()))
    total = 0
    for stone in stones:
        total += blink_count(stone, 75)
    return total

@cache
def blink_count(stone, blinks):
    if blinks == 0:
        return 1
    if stone == 0:
        return blink_count(1, blinks - 1)
    s = str(stone)
    if len(s) % 2 == 0:
        mid = len(s) // 2
        left = int(s[:mid])
        right = int(s[mid:])
        return blink_count(left, blinks - 1) + blink_count(right, blinks - 1)
    return blink_count(stone * 2024, blinks - 1)

samples = [
    ("125 17", 533081565861)
]

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part2(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 2: {sample_result} ----")

with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part2(lines)
print(f"---- Final result Part 2: {final_result} ----")

