import sys

def parse_input(lines):
    # Register A: <value>
    # Register B: 0
    # Register C: 0
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
    
    # Work backwards to find the minimum A
    # The key insight: we can reverse engineer the program by working backwards
    # from the required output to find the initial A value
    
    def simulate_with_A(test_A):
        output = run_program(test_A, 0, 0, program)
        return output == program
    
    # Optimization: work backwards from the program structure
    # The program uses adv instructions which divide by powers of 2
    # We can build up the answer by considering what A needs to be at each step
    
    # Start with the final state and work backwards
    # At the end, A should be 0, and we need to reverse the operations
    
    # For each adv instruction (opcode 0), if we have A // (2^operand) = result,
    # then to reverse it: previous_A = result * (2^operand) + remainder
    # where 0 <= remainder < (2^operand)
    
    # We'll use a recursive approach to explore possible A values
    def find_min_A(ip, current_A, current_B, current_C, min_found):
        if ip >= len(program):
            # Check if this A value produces the correct output
            if simulate_with_A(current_A):
                return current_A
            return None
        
        opcode = program[ip]
        operand = program[ip + 1]
        
        # Try to reverse the operation
        if opcode == 0:  # adv
            # A // (2^operand) = current_A
            # So previous_A = current_A * (2^operand) + remainder
            base = current_A * (2 ** combo_value(operand, current_A, current_B, current_C))
            for remainder in range(2 ** combo_value(operand, current_A, current_B, current_C)):
                prev_A = base + remainder
                if prev_A < min_found:
                    result = find_min_A(ip + 2, prev_A, current_B, current_C, min_found)
                    if result is not None:
                        min_found = min(min_found, result)
                        return result
        elif opcode == 1:  # bxl
            # B = B ^ operand
            # To reverse: previous_B = B ^ operand
            prev_B = current_B ^ operand
            result = find_min_A(ip + 2, current_A, prev_B, current_C, min_found)
            if result is not None:
                return result
        elif opcode == 2:  # bst
            # B = combo_value(operand) % 8
            # This overwrites B, so we can't easily reverse it
            # Try all possible previous B values
            for prev_B in range(8):
                result = find_min_A(ip + 2, current_A, prev_B, current_C, min_found)
                if result is not None:
                    return result
        elif opcode == 3:  # jnz
            # If A != 0, jump to operand
            # This is conditional, hard to reverse
            # Try both cases
            if current_A != 0:
                # Jumped case
                result = find_min_A(operand, current_A, current_B, current_C, min_found)
                if result is not None:
                    return result
            # Didn't jump case
            result = find_min_A(ip + 2, current_A, current_B, current_C, min_found)
            if result is not None:
                return result
        elif opcode == 4:  # bxc
            # B = B ^ C
            # To reverse: previous_B = B ^ C
            prev_B = current_B ^ current_C
            result = find_min_A(ip + 2, current_A, prev_B, current_C, min_found)
            if result is not None:
                return result
        elif opcode == 5:  # out
            # Output combo_value(operand) % 8
            # This should match program[ip+1] % 8
            expected_output = program[ip + 1] % 8
            actual_output = combo_value(operand, current_A, current_B, current_C) % 8
            if actual_output == expected_output:
                result = find_min_A(ip + 2, current_A, current_B, current_C, min_found)
                if result is not None:
                    return result
        elif opcode == 6:  # bdv
            # B = A // (2^operand)
            # To reverse: previous_A = B * (2^operand) + remainder
            base = current_B * (2 ** combo_value(operand, current_A, current_B, current_C))
            for remainder in range(2 ** combo_value(operand, current_A, current_B, current_C)):
                prev_A = base + remainder
                if prev_A < min_found:
                    result = find_min_A(ip + 2, prev_A, current_B, current_C, min_found)
                    if result is not None:
                        min_found = min(min_found, result)
                        return result
        elif opcode == 7:  # cdv
            # C = A // (2^operand)
            # To reverse: previous_A = C * (2^operand) + remainder
            base = current_C * (2 ** combo_value(operand, current_A, current_B, current_C))
            for remainder in range(2 ** combo_value(operand, current_A, current_B, current_C)):
                prev_A = base + remainder
                if prev_A < min_found:
                    result = find_min_A(ip + 2, prev_A, current_B, current_C, min_found)
                    if result is not None:
                        min_found = min(min_found, result)
                        return result
        
        return None
    
    # Start the search from the end with A=0, B=0, C=0
    result = find_min_A(0, 0, 0, 0, float('inf'))
    if result is not None:
        return result
    
    # Fallback: try a more direct approach
    # Since the program outputs itself, we can try to construct A step by step
    test_A = 1
    while test_A < 1000000000:  # 1 billion upper bound
        if simulate_with_A(test_A):
            return test_A
        test_A += 1
    
    return -1

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
