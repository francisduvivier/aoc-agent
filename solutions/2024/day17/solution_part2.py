# Edit this file: implement solve_part2

def solve_part2(lines):
    # Parse the program from the input
    for line in lines:
        if line.startswith("Program:"):
            program_str = line.split(": ")[1]
            P = list(map(int, program_str.split(",")))
            break
    
    # Find possible A that produce P as output
    possible = {0}
    for target in reversed(P):
        new_possible = set()
        for a in possible:
            for d in range(8):
                b = d ^ 3
                c = (a * 8 + d) // (1 << b)
                out = ((b ^ 5) ^ c) % 8
                if out == target:
                    new_possible.add(a * 8 + d)
        possible = new_possible
    return min(possible)

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
