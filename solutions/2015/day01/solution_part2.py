def main():
    sample_input = "()())"
    sample_answer = 5

    with open('input.txt', 'r') as f:
        instructions = f.read().strip()

    floor = 0
    pos = 0
    for i, char in enumerate(instructions, start=1):
        if char == '(':
            floor += 1
        elif char == ')':
            floor -= 1
        if floor == -1:
            pos = i
            break

    sample_floor = 0
    sample_pos = 0
    for i, char in enumerate(sample_input, start=1):
        if char == '(':
            sample_floor += 1
        elif char == ')':
            sample_floor -= 1
        if sample_floor == -1:
            sample_pos = i
            break

    print(f"---- Sample Solution Part 2: {sample_pos} ----")
    print(f"---- Final Solution Part 2: {pos} ----")

if __name__ == "__main__":
    main()
