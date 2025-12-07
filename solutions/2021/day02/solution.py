with open('input.txt') as f:
    cmds = [line.strip().split() for line in f if line.strip()]

h1, d1 = 0, 0
for dir, x in cmds:
    x = int(x)
    if dir == 'forward': h1 += x
    elif dir == 'down': d1 += x
    elif dir == 'up': d1 -= x
print(h1 * d1)

h2, d2, aim = 0, 0, 0
for dir, x in cmds:
    x = int(x)
    if dir == 'forward':
        h2 += x
        d2 += aim * x
    elif dir == 'down': aim += x
    elif dir == 'up': aim -= x
print(h2 * d2)
