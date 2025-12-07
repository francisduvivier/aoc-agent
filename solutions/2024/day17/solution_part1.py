def solve_part1(lines):
    # Parse registers
    A = int(lines[0].split(': ')[1])
    B = int(lines[1].split(': ')[1])
    C = int(lines[2].split(': ')[1])
    
    # Parse program
    program = list(map(int, lines[4].split(': ')[1].split(',')))
    
    # Run program
    ip = 0
    output = []
    
    while ip < len(program):
        opcode = program[ip]
        operand = program[ip + 1]
        
        if opcode == 0:  # adv
            if operand <= 3:
                denom = 1 << operand
            elif operand == 4:
                denom = 1 << A
            elif operand == 5:
                denom = 1 << B
            elif operand == 6:
                denom = 1 << C
            A = A // denom
            ip += 2
            
        elif opcode == 1:  # bxl
            B = B ^ operand
            ip += 2
            
        elif opcode == 2:  # bst
            if operand <= 3:
                val = operand
            elif operand == 4:
                val = A
            elif operand == 5:
                val = B
            elif operand == 6:
                val = C
            B = val % 8
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
            if operand <= 3:
                val = operand
            elif operand == 4:
                val = A
            elif operand == 5:
                val = B
            elif operand == 6:
                val = C
            output.append(str(val % 8))
            ip += 2
            
        elif opcode == 6:  # bdv
            if operand <= 3:
                denom = 1 << operand
            elif operand == 4:
                denom = 1 << A
            elif operand == 5:
                denom = 1 << B
            elif operand == 6:
                denom = 1 << C
            B = A // denom
            ip += 2
            
        elif opcode == 7:  # cdv
            if operand <= 3:
                denom = 1 << operand
            elif operand == 4:
                denom = 1 << A
            elif operand == 5:
                denom = 1 << B
            elif operand == 6:
                denom = 1 << C
            C = A // denom
            ip += 2
    
    return ','.join(output)

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples.
samples = [
    ("""Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0""", "4,6,3,5,6,3,5,2,1,0")
]  # TODO: fill with actual samples and expected results

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part1(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 1: {sample_result} ----") # YOU MUST NOT change this output format

# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part1(lines)
print(f"---- Final result Part 1: {final_result} ----") # YOU MUST NOT change this output format
