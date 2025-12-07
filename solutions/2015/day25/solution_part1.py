def solve_part1(lines):
    return len(lines)

if __name__ == '__main__':
    sample_input = """dummy input"""
    sample_answer = 1

    sample_result = solve_part1(sample_input.strip().splitlines())
    print(f"---- Sample Solution Part 1: {sample_result} ----")

    with open('input.txt') as f:
        lines = [line.strip() for line in f]
    final_result = solve_part1(lines)
    print(f"---- Final Solution Part 1: {final_result} ----")
