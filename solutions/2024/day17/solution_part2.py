# Edit this file: implement solve_part2

def solve_part2(lines):
    # Parse registers and program
    A = int(lines[0].split(": ")[1])
    B = int(lines[1].split(": ")[1])
    C = int(lines[2].split(": ")[1])
    program = list(map(int, lines[4].split(": ")[1].split(",")))
    
    # Function to get value of a combo operand
    def get_combo_value(operand):
        if operand <= 3:
            return operand
        elif operand == 4:
            return A
        elif operand == 5:
            return B
        elif operand == 6:
            return C
        else:
            return 0
    
    # Run the program and collect output
    ip = 0
    output = []
    
    while ip < len(program):
        opcode = program[ip]
        operand = program[ip + 1]
        
        if opcode == 0:  # adv
            A = A // (2 ** get_combo_value(operand))
            ip += 2
        elif opcode == 1:  # bxl
            B = B ^ operand
            ip += 2
        elif opcode == 2:  # bst
            B = get_combo_value(operand) % 8
            ip += 2
        elif opcode == 3:  # jnz
            if A != 0:
                ip = operand
            else:
                ip += 2
        elif opcode == 4:  # bxc
            B = B ^ C
            ip += 2
        elif opcode == 5:  # out
            output.append(get_combo_value(operand) % 8)
            ip += 2
        elif opcode == 6:  # bdv
            A_val = A // (2 ** get_combo_value(operand))
            B = A_val
            ip += 2
        elif opcode == 7:  # cdv
            A_val = A // (2 ** get_combo_value(operand))
            C = A_val
            ip += 2
        else:
            break
    
    return ",".join(map(str, output))

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples IF there are any samples given for part 2.
samples = []  # TODO: fill with actual samples and expected results

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

