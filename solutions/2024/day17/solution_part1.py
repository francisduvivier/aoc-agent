# Edit this file: implement solve_part1

def solve_part1(lines):
    # Parse registers
    a = int(lines[0].split(": ")[1])
    b = int(lines[1].split(": ")[1])
    c = int(lines[2].split(": ")[1])
    
    # Parse program
    program = list(map(int, lines[4].split(": ")[1].split(",")))
    
    # Run program
    ip = 0
    output = []
    
    while ip < len(program):
        opcode = program[ip]
        operand = program[ip + 1]
        
        if opcode == 0:  # adv
            denom = 1 << combo_value(operand, a, b, c)
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
            denom = 1 << combo_value(operand, a, b, c)
            b = a // denom
            ip += 2
        elif opcode == 7:  # cdv
            denom = 1 << combo_value(operand, a, b, c)
            c = a // denom
            ip += 2
    
    return ",".join(map(str, output))

def combo_value(operand, a, b, c):
    if operand <= 3:
        return operand
    elif operand == 4:
        return a
    elif operand == 5:
        return b
    elif operand == 6:
        return c
    return 0

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples.
samples = [
    ("""Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0""", "4,6,3,5,6,3,5,2,1,0")
]

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part1(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 1: {sample_result} ----") # YOU MUST NOT change this output format

# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part1(lines)
print(f"---- Final result Part 1: {final_result} ----") # YOU MUST NOT change this output format

