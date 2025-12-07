# Edit this file: implement solve_part2

def solve_part2(lines):
    dial = 50
    count = 0
    for line in lines:
        direction = line[0]
        distance = int(line[1:])
        if direction == 'L':
            # Moving left: count how many times we pass 0
            # From dial to dial - distance (mod 100)
            # We pass 0 if we cross from 0 to 99 (i.e., going from 0 to 99)
            # This happens if dial >= distance: we go dial, dial-1, ..., 0, 99, ...
            # Actually, we pass 0 if we start at dial and go left by distance and cross the boundary
            # We cross the boundary if dial < distance (because we go negative)
            # In that case, we pass 0 exactly once during the rotation
            # Plus, if we end exactly at 0, that's another count
            new_dial = (dial - distance) % 100
            if dial < distance:
                count += 1
            if new_dial == 0:
                count += 1
            dial = new_dial
        else:  # direction == 'R'
            # Moving right: count how many times we pass 0
            # We pass 0 if we cross from 99 to 0
            # This happens if dial + distance > 99
            # In that case, we pass 0 exactly once during the rotation
            # Plus, if we end exactly at 0, that's another count
            new_dial = (dial + distance) % 100
            if dial + distance > 99:
                count += 1
            if new_dial == 0:
                count += 1
            dial = new_dial
    return count

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples IF there are any samples given for part 2.
samples = [
    ("L68\nL30\nR48\nL5\nR60\nL55\nL1\nL99\nR14\nL82", 6)
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

