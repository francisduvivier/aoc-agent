def solve_part2(lines):
    sequence = lines[0]
    for _ in range(50):
        new_sequence = []
        count = 1
        for i in range(1, len(sequence)):
            if sequence[i] == sequence[i-1]:
                count += 1
            else:
                new_sequence.append(str(count))
                new_sequence.append(sequence[i-1])
                count = 1
        new_sequence.append(str(count))
        new_sequence.append(sequence[-1])
        sequence = ''.join(new_sequence)
    return len(sequence)

if __name__ == '__main__':
    sample_input = """1"""
    sample_answer = 2
    
    sample_result = solve_part2(sample_input.strip().splitlines())
    print(f"---- Sample Solution Part 2: {sample_result} ----")
    
    with open('input.txt') as f:
        lines = [line.strip() for line in f]
    final_result = solve_part2(lines)
    print(f"---- Final Solution Part 2: {final_result} ----")
