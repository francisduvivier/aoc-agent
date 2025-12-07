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

def combo_value(operand, a, b, c):
    if operand <= 3:
        return operand
    elif operand == 4:
        return a
    elif operand == 5:
        return b
    elif operand == 6:
        return c
    else:
        raise ValueError("Invalid combo operand")

def run_program(a, b, c, program):
    ip = 0
    output = []
    while ip < len(program):
        opcode = program[ip]
        operand = program[ip+1]
        if opcode == 0:  # adv
            denom = 2 ** combo_value(operand, a, b, c)
            a = a // denom
            ip += 2
        elif opcode == 1:  # bxl
            b = b ^ operand
            ip += 2
        elif opcode == 2:  # bst
            b = combo_value(operand, a, b, c) % 8
            ip += 2
        elif opcode == 3:  # jnz
            if a != 0:
                ip = operand
            else:
                ip += 2
        elif opcode == 4:  # bxc
            b = b ^ c
            ip += 2
        elif opcode == 5:  # out
            output.append(combo_value(operand, a, b, c) % 8)
            ip += 2
        elif opcode == 6:  # bdv
            denom = 2 ** combo_value(operand, a, b, c)
            b = a // denom
            ip += 2
        elif opcode == 7:  # cdv
            denom = 2 ** combo_value(operand, a, b, c)
            c = a // denom
            ip += 2
        else:
            raise ValueError("Invalid opcode")
    return output

def solve_part2(lines):
    a, b, c, program = parse_input(lines)
    
    # We need to find the minimal A such that output == program.
    # The program uses adv (opcode 0) and cdv (opcode 7) which divide A by powers of 2.
    # The output is determined by combo operands modulo 8.
    # We can reverse-engineer the required A by working backwards through the program.
    
    # The key insight: the output is determined by the lowest 3 bits of A at each step.
    # We can build A bit by bit from the least significant bits.
    
    def check_a(candidate_a):
        out = run_program(candidate_a, 0, 0, program)
        return out == program
    
    # Start with small values and increment until we find a match
    # Optimization: we can build the answer bit by bit
    candidate = 0
    bit_pos = 0
    
    while True:
        if check_a(candidate):
            return candidate
        # Try setting the next bit
        candidate |= (1 << bit_pos)
        if check_a(candidate):
            return candidate
        # Clear that bit and try next position
        candidate &= ~(1 << bit_pos)
        bit_pos += 1
        
        # Safety check to avoid infinite loop
        if bit_pos > 60:
            break
    
    # Fallback: brute force from 1 upward (shouldn't reach here for valid inputs)
    for candidate in range(1, 1000000):
        if check_a(candidate):
            return candidate
    
    return -1  # No solution found

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples IF there are any samples given for part 2.
samples = [
    ("""Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0""", 117440)
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
