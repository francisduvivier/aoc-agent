import sys

def parse_input(lines):
    # Register A: 21539243
    # Register B: 0
    # Register C: 0
    #
    # Program: 2,4,1,3,7,5,1,5,0,3,4,1,5,5,3,0
    a = int(lines[0].split(":")[1].strip())
    b = int(lines[1].split(":")[1].strip())
    c = int(lines[2].split(":")[1].strip())
    program = [int(x) for x in lines[4].split(":")[1].strip().split(",")]
    return a, b, c, program

def run_program(a, b, c, program):
    registers = [a, b, c]
    ip = 0
    output = []
    while ip < len(program):
        opcode = program[ip]
        operand = program[ip + 1]
        if opcode == 0:  # adv
            combo_val = get_combo_value(operand, registers)
            registers[0] = registers[0] // (2 ** combo_val)
            ip += 2
        elif opcode == 1:  # bxl
            registers[1] = registers[1] ^ operand
            ip += 2
        elif opcode == 2:  # bst
            combo_val = get_combo_value(operand, registers)
            registers[1] = combo_val % 8
            ip += 2
        elif opcode == 3:  # jnz
            if registers[0] != 0:
                ip = operand
            else:
                ip += 2
        elif opcode == 4:  # bxc
            registers[1] = registers[1] ^ registers[2]
            ip += 2
        elif opcode == 5:  # out
            combo_val = get_combo_value(operand, registers)
            output.append(combo_val % 8)
            ip += 2
        elif opcode == 6:  # bdv
            combo_val = get_combo_value(operand, registers)
            registers[1] = registers[0] // (2 ** combo_val)
            ip += 2
        elif opcode == 7:  # cdv
            combo_val = get_combo_value(operand, registers)
            registers[2] = registers[0] // (2 ** combo_val)
            ip += 2
        else:
            break
    return output

def get_combo_value(operand, registers):
    if operand <= 3:
        return operand
    elif operand == 4:
        return registers[0]
    elif operand == 5:
        return registers[1]
    elif operand == 6:
        return registers[2]
    else:
        return 0

def solve_part2(lines):
    a, b, c, program = parse_input(lines)
    # We need to find the lowest positive initial value for register A
    # that causes the program to output a copy of itself.
    
    # The program is short (16 instructions). We can try to reverse engineer
    # the required A value by working backwards from the program.
    
    # The program outputs are the result of 'out' instructions with combo operands.
    # We need to find A such that the output sequence equals the program sequence.
    
    # Let's try a brute force approach with some optimizations.
    # Since the program uses division by powers of 2, A values will decrease rapidly.
    
    # We can use the fact that the program is deterministic and try to find
    # a pattern or use dynamic programming.
    
    # For this specific problem, we can work backwards:
    # The last output should match the last program instruction.
    # We can build up the required A value step by step.
    
    def check_a_value(test_a):
        output = run_program(test_a, b, c, program)
        return output == program
    
    # Start with a reasonable search space
    # The program uses division by powers of 2, so A values can be large
    for test_a in range(1, 10000000):  # Try up to 10 million
        if check_a_value(test_a):
            return test_a
    
    return -1  # Not found in search space

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
