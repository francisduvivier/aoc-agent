def main():
    with open('input.txt') as f:
        lines = f.read().splitlines()

    if not lines:
        print("0\n0")
        return

    max_len = max(len(line) for line in lines)
    padded_lines = [line.ljust(max_len) for line in lines]
    columns = list(zip(*padded_lines))

    separators = [i for i, col in enumerate(columns) if all(c == ' ' for c in col)]
    regions = []
    start = 0
    for i in range(len(columns)):
        if i in separators:
            if start < i:
                regions.append((start, i - 1))
            start = i + 1
    if start < len(columns):
        regions.append((start, len(columns) - 1))

    # Part 1: process regions left to right, columns left to right
    part1_total = 0
    for start, end in regions:
        problem_cols = [columns[i] for i in range(start, end + 1)]
        op = None
        for col in problem_cols:
            if col[-1] != ' ':
                op = col[-1]
                break
        if op is None:
            continue
        nums = []
        for col in problem_cols:
            digits = []
            for c in col[:-1]:
                if c != ' ':
                    digits.append(c)
            if digits:
                nums.append(int(''.join(digits)))
            else:
                nums.append(0)
        if op == '+':
            res = sum(nums)
        elif op == '*':
            res = 1
            for n in nums:
                res *= n
        else:
            res = 0
        part1_total += res

    # Part 2: process regions right to left, columns right to left within each region
    part2_total = 0
    for start, end in reversed(regions):
        problem_cols = [columns[i] for i in range(start, end + 1)]
        op = None
        for col in problem_cols:
            if col[-1] != ' ':
                op = col[-1]
                break
        if op is None:
            continue
        nums = []
        for col in reversed(problem_cols):
            digits = []
            for c in col[:-1]:
                if c != ' ':
                    digits.append(c)
            if digits:
                nums.append(int(''.join(digits)))
            else:
                nums.append(0)
        if op == '+':
            res = sum(nums)
        elif op == '*':
            res = 1
            for n in nums:
                res *= n
        else:
            res = 0
        part2_total += res

    print(part1_total)
    print(part2_total)

if __name__ == "__main__":
    main()
