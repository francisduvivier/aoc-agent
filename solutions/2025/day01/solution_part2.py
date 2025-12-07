def solve_part2(lines):
    current = 50
    total = 0

    for line in lines:
        direction = line[0]
        distance = int(line[1:])
        if direction == 'R':
            remainder = current % 100
            if remainder == 0:
                first_i = 100
            else:
                first_i = 100 - remainder
            if first_i > distance:
                count = 0
            else:
                count = (distance - first_i) // 100 + 1
            current = (current + distance) % 100
        else:  # 'L'
            remainder = current % 100
            if remainder == 0:
                first_i = 100
            else:
                first_i = remainder
            if first_i > distance:
                count = 0
            else:
                count = (distance - first_i) // 100 + 1
            current = (current - distance) % 100
        total += count

    return total

samples = [
    ("""L68
L30
R48
L5
R60
L55
L1
L99
R14
L82""", 6)
]

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part2(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 2: {sample_result} ----")

with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part2(lines)
print(f"---- Final result Part 2: {final_result} ----")
