# Edit this file: implement solve_part2

def solve_part2(lines):
    dial = 50
    count = 0
    for line in lines:
        direction = line[0]
        distance = int(line[1:])
        if direction == 'L':
            # Moving left: each click decreases the dial by 1 (wrapping from 0 to 99)
            for _ in range(distance):
                dial = (dial - 1) % 100
                if dial == 0:
                    count += 1
        else:  # direction == 'R'
            # Moving right: each click increases the dial by 1 (wrapping from 99 to 0)
            for _ in range(distance):
                dial = (dial + 1) % 100
                if dial == 0:
                    count += 1
    return count

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples IF there are any samples given for part 2.
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

