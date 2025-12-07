# Edit this file: implement solve_part2

def solve_part2(lines):
    A = B = C = 0
    prog = []
    for line in lines:
        if line.startswith("Register A:"):
            A = int(line.split(": ")[1])
        elif line.startswith("Register B:"):
            B = int(line.split(": ")[1])
        elif line.startswith("Register C:"):
            C = int(line.split(": ")[1])
        elif line.startswith("Program:"):
            prog = list(map(int, line.split(": ")[1].split(",")))
    
    S = prog
    
    def compute_output(A):
        B = A % 8
        B ^= 3
        C = A // (2 ** B)
        B ^= 5
        B ^= C
        return B % 8
    
    possible_A = [0]
    for target in reversed(S):
        new_possible = []
        for prev in possible_A:
            for r in range(8):
                cand_A = 8 * prev + r
                if compute_output(cand_A) == target:
                    new_possible.append(cand_A)
        possible_A = new_possible
    return min(possible_A)

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples IF there are any samples given for part 2.
samples = [
    ("""Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0""", 117440)
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
