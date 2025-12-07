# Edit this file: implement solve_part2

def solve_part2(lines):
    # Parse input
    A = int(lines[0].split(": ")[1])
    B = int(lines[1].split(": ")[1])
    C = int(lines[2].split(": ")[1])
    program = list(map(int, lines[4].split(": ")[1].split(",")))
    
    # Helper to get operand value
    def get_val(operand, regs):
        if operand <= 3:
            return operand
        elif operand == 4:
            return regs[0]
        elif operand == 5:
            return regs[1]
        elif operand == 6:
            return regs[2]
        else:
            return None
    
    # Simulate execution
    regs = [A, B, C]
    ip = 0
    output = []
    
    while ip < len(program):
        opcode = program[ip]
        operand = program[ip + 1]
        
        if opcode == 0:  # adv
            denom = 1 << get_val(operand, regs)
            if denom != 0:
                regs[0] = regs[0] // denom
            ip += 2
        elif opcode == 1:  # bxl
            regs[1] = regs[1] ^ operand
            ip += 2
        elif opcode == 2:  # bst
            regs[1] = get_val(operand, regs) % 8
            ip += 2
        elif opcode == 3:  # jnz
            if regs[0] != 0:
                ip = operand
            else:
                ip += 2
        elif opcode == 4:  # bxc
            regs[1] = regs[1] ^ regs[2]
            ip += 2
        elif opcode == 5:  # out
            output.append(get_val(operand, regs) % 8)
            ip += 2
        elif opcode == 6:  # bdv
            denom = 1 << get_val(operand, regs)
            if denom != 0:
                regs[1] = regs[0] // denom
            ip += 2
        elif opcode == 7:  # cdv
            denom = 1 << get_val(operand, regs)
            if denom != 0:
                regs[2] = regs[0] // denom
            ip += 2
        else:
            break
    
    return ",".join(map(str, output))

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples IF there are any samples given for part 2.
samples = [
    ("""Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0""", "0,3,5,4,3,0")
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

