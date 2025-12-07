# Edit this file: implement solve_part2

def solve_part2(lines):
    # Parse the program
    for line in lines:
        if line.startswith("Program: "):
            program = list(map(int, line.split(": ")[1].split(",")))
            break
    
    def find_x(current_A, desired_o):
        for x in range(8):
            A = current_A * 8 + x
            B = A % 8
            B ^= 3
            C = A // (2 ** B)
            B ^= 5
            B ^= C
            output = B % 8
            if output == desired_o:
                yield x
    
    possible_current = {0}
    for i in range(len(program) - 1, -1, -1):
        new_possible = set()
        for curr in possible_current:
            for x in find_x(curr, program[i]):
                new_possible.add(curr * 8 + x)
        possible_current = new_possible
    return min(possible_current) if possible_current else 0

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples IF there are any samples given for part 2.
samples = []  # TODO: fill with actual samples and expected results

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part2(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 2: {sample_result} ----") # YOU MUST NOT change this output format
print("---- Sample NONE result Part 2: NONE ----") # Uncomment this if no samples are given for part 2
# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part2(lines)
print(f"---- Final result Part 2: {final_result} ----") # YOU MUST NOT change this output format
