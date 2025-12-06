with open('input.txt') as f:
    lines = [line.rstrip('\n') for line in f]

max_len = max(len(line) for line in lines)
padded_lines = [line.ljust(max_len) for line in lines]

columns = list(zip(*padded_lines))

separator_indices = []
for i, col in enumerate(columns):
    if all(c == ' ' for c in col):
        separator_indices.append(i)

problems = []
current = []
for i, col in enumerate(columns):
    if i in separator_indices:
        if current:
            problems.append(current)
            current = []
    else:
        current.append(col)
if current:
    problems.append(current)

total = 0
for problem in problems:
    numbers = []
    for col in problem:
        digits = []
        for c in col[:-1]:
            if c != ' ':
                digits.append(c)
        num_str = ''.join(digits)
        num = int(num_str) if num_str else 0
        numbers.append(num)
    
    op = None
    for col in problem:
        if col[-1] != ' ':
            op = col[-1]
            break
    
    if op is None:
        continue
    
    numbers_rev = list(reversed(numbers))
    result = numbers_rev[0]
    for num in numbers_rev[1:]:
        if op == '+':
            result += num
        elif op == '*':
            result *= num
    total += result

print(total)
