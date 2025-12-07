# Edit this file: implement solve_part2

def solve_part2(lines):
    # Parse input
    A = int(lines[0].split(': ')[1])
    B = int(lines[1].split(': ')[1])
    C = int(lines[2].split(': ')[1])
    program = list(map(int, lines[4].split(': ')[1].split(',')))
    
    target = program
    
    def find_possible_A(index):
        if index == len(target):
            return [0]
        possible = []
        for prev_A in find_possible_A(index + 1):
            for x in range(8):
                A_val = 8 * prev_A + x
                y = x ^ 3
                C_val = A_val // (2 ** y)
                B_val = (y ^ 5) ^ C_val
                out = B_val % 8
                if out == target[-(index + 1)]:
                    possible.append(A_val)
        return possible
    
    possible_A = find_possible_A(0)
    return min(a for a in possible_A if a > 0)

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
