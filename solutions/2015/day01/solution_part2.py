with open('input.txt') as f:
    instructions = f.read().strip()

floor = 0
for i, c in enumerate(instructions, 1):
    floor += 1 if c == '(' else -1
    if floor == -1:
        print(i)
        break
