# Edit this file: implement solve_part2

def solve_part2(lines):
    for line in lines:
        if line.startswith("Program:"):
            prog = list(map(int, line.split(': ')[1].split(',')))
            break
    P = prog
    possible_A = {P[-1] ^ 3 ^ 5}
    for target_D in reversed(P[:-1]):
        new_possible = set()
        for a in possible_A:
            for x in range(8):
                shift = 1 << (x ^ 3)
                c = a // shift
                if (x ^ 3 ^ 5) ^ c == target_D:
                    new_a = a * 8 + x
                    new_possible.add(new_a)
        possible_A = new_possible
    return min(possible_A)

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples IF there are any samples given for part 2.
samples = [
    ("Register A: 2024\nRegister B: 0\nRegister C: 0\n\nProgram: 0,3,5,4,3,0", 117440)
]

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
