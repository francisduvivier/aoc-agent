def solve_part1(lines):
    sequence = lines[0]
    for _ in range(40):
        new_sequence = []
        i = 0
        while i < len(sequence):
            count = 1
            while i + count < len(sequence) and sequence[i] == sequence[i + count]:
                count += 1
            new_sequence.append(str(count))
            new_sequence.append(sequence[i])
            i += count
        sequence = ''.join(new_sequence)
    return len(sequence)

if __name__ == '__main__':
    sample_input = """1"""
    sample_answer = 82350

    sample_result = solve_part1(sample_input.strip().splitlines())
    print(f"---- Sample Solution Part 1: {sample_result} ----")

    with open('input.txt') as f:
        lines = [line.strip() for line in f]
    final_result = solve_part1(lines)
    print(f"---- Final Solution Part 1: {final_result} ----")
