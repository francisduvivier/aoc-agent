# Edit this file: implement solve_part2

def solve_part2(lines):
    # Parse registers and program
    A = int(lines[0].split(': ')[1])
    B = int(lines[1].split(': ')[1])
    C = int(lines[2].split(': ')[1])
    program = [int(x) for x in lines[4].split(': ')[1].split(',')]
    
    # We need to find the lowest positive initial value for register A
    # that causes the program to output a copy of itself
    
    def simulate(A_val):
        registers = [A_val, B, C]
        output = []
        ip = 0
        
        while ip < len(program):
            opcode = program[ip]
            operand = program[ip + 1]
            
            if opcode == 0:  # adv
                registers[0] = registers[0] // (2 ** combo_value(operand, registers))
                ip += 2
            elif opcode == 1:  # bxl
                registers[1] = registers[1] ^ operand
                ip += 2
            elif opcode == 2:  # bst
                registers[1] = combo_value(operand, registers) % 8
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
                output.append(combo_value(operand, registers) % 8)
                ip += 2
            elif opcode == 6:  # bdv
                registers[1] = registers[0] // (2 ** combo_value(operand, registers))
                ip += 2
            elif opcode == 7:  # cdv
                registers[2] = registers[0] // (2 ** combo_value(operand, registers))
                ip += 2
        
        return output
    
    def combo_value(operand, registers):
        if operand <= 3:
            return operand
        elif operand == 4:
            return registers[0]
        elif operand == 5:
            return registers[1]
        elif operand == 6:
            return registers[2]
        else:
            raise ValueError("Invalid combo operand")
    
    # Try to find the minimal A value that produces the program as output
    # We'll use a reverse engineering approach to build up the answer
    def find_min_A():
        # Start with the last instruction and work backwards
        # The program needs to output exactly the program sequence
        target_output = program
        
        # We'll build the answer by checking candidates
        # Since the program uses division by powers of 2, we can work backwards
        # from the end to find minimal values
        
        # For this specific problem, we need to find A such that
        # the output equals the program
        
        # Try a reasonable search space
        for A_candidate in range(1, 10000000):  # Search up to 10 million
            output = simulate(A_candidate)
            if output == target_output:
                return A_candidate
        
        return None
    
    result = find_min_A()
    return result

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

