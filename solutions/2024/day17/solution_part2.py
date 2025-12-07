# Edit this file: implement solve_part2

def get_combo(operand, A, B, C):
    if operand <= 3:
        return operand
    elif operand == 4:
        return A
    elif operand == 5:
        return B
    elif operand == 6:
        return C
    else:
        raise ValueError("Invalid operand")

def run_iteration(A, B, C, program):
    output = []
    IP = 0
    while IP < len(program):
        opcode = program[IP]
        operand = program[IP + 1]
        if opcode == 0:  # adv
            combo = get_combo(operand, A, B, C)
            A = A // (1 << combo)
        elif opcode == 1:  # bxl
            B = B ^ operand
        elif opcode == 2:  # bst
            combo = get_combo(operand, A, B, C)
            B = combo % 8
        elif opcode == 3:  # jnz
            if A != 0:
                IP = operand
                continue
            else:
                IP += 2
                break
        elif opcode == 4:  # bxc
            B = B ^ C
        elif opcode == 5:  # out
            combo = get_combo(operand, A, B, C)
            output.append(combo % 8)
            IP += 2
            if len(output) == 1:
                break
        elif opcode == 6:  # bdv
            combo = get_combo(operand, A, B, C)
            B = A // (1 << combo)
        elif opcode == 7:  # cdv
            combo = get_combo(operand, A, B, C)
            C = A // (1 << combo)
        else:
            IP += 2
    return output[0] if output else None, A, B, C

def find_A(remaining, B, C, current_A, program):
    if not remaining:
        return current_A
    target = remaining[0]
    for a in range(8):
        full_A = current_A * 8 + a
        out, new_A, new_B, new_C = run_iteration(full_A, B, C, program)
        if out == target:
            if not remaining[1:]:
                if new_A == 0:
                    return full_A
            else:
                sub = find_A(remaining[1:], new_B, new_C, new_A, program)
                if sub is not None:
                    return sub
    return None

def solve_part2(lines):
    program_str = lines[4].split(': ')[1]
    program = [int(x) for x in program_str.split(',')]
    P = program
    remaining = P[::-1]
    result = find_A(remaining, 0, 0, 0, program)
    return result

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
