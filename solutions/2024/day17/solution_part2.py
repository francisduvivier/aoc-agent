import sys

def parse_input(lines):
    # Register A: <value>
    # Register B: <value>
    # Register C: <value>
    # (blank line)
    # Program: <comma-separated numbers>
    a_line = lines[0]
    b_line = lines[1]
    c_line = lines[2]
    program_line = lines[4]
    
    A = int(a_line.split(":")[1].strip())
    B = int(b_line.split(":")[1].strip())
    C = int(c_line.split(":")[1].strip())
    
    program = [int(x) for x in program_line.split(":")[1].strip().split(",")]
    
    return A, B, C, program

def combo_value(operand, A, B, C):
    if operand <= 3:
        return operand
    elif operand == 4:
        return A
    elif operand == 5:
        return B
    elif operand == 6:
        return C
    else:
        raise ValueError(f"Invalid combo operand: {operand}")

def run_program(A, B, C, program):
    ip = 0
    output = []
    
    while ip < len(program):
        opcode = program[ip]
        operand = program[ip + 1]
        
        if opcode == 0:  # adv
            denom = 2 ** combo_value(operand, A, B, C)
            A = A // denom
            ip += 2
        elif opcode == 1:  # bxl
            B = B ^ operand
            ip += 2
        elif opcode == 2:  # bst
            B = combo_value(operand, A, B, C) % 8
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
            output.append(combo_value(operand, A, B, C) % 8)
            ip += 2
        elif opcode == 6:  # bdv
            denom = 2 ** combo_value(operand, A, B, C)
            B = A // denom
            ip += 2
        elif opcode == 7:  # cdv
            denom = 2 ** combo_value(operand, A, B, C)
            C = A // denom
            ip += 2
        else:
            raise ValueError(f"Invalid opcode: {opcode}")
    
    return output

def solve_part2(lines):
    A, B, C, program = parse_input(lines)
    
    # We need to find the minimum positive A that makes the program output itself
    # This is a reverse engineering problem. We can work backwards from the program.
    
    # The key insight: the program uses adv instructions (opcode 0) which divide A by powers of 2.
    # We can reverse the computation to find the original A value.
    
    # Let's try a different approach: brute force with optimization
    # We'll start from a reasonable lower bound and work up
    
    def check_A_value(test_A):
        output = run_program(test_A, 0, 0, program)
        return output == program
    
    # Start with a reasonable lower bound
    # The program length gives us a hint about the magnitude needed
    lower_bound = 1
    
    # Try to find a pattern or use mathematical reasoning
    # For adv instructions, if we have A // (2^operand) = result, then A = result * (2^operand)
    # Working backwards from the end state (A=0) to find the initial A
    
    # Let's implement a more sophisticated search
    # We'll use the fact that the program must output itself
    
    # Start with a reasonable search space
    for test_A in range(lower_bound, 100000000):  # 100 million upper bound
        if check_A_value(test_A):
            return test_A
    
    return -1  # Not found in reasonable range

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
