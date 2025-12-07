with open('input.txt') as f:
    rotations = [line.strip() for line in f.readlines()]

pos = 50
p1 = 0
p2 = 0
for r in rotations:
    if not r:
        continue
    dirc = 1 if r[0] == 'R' else -1
    dist = int(r[1:])
    for _ in range(dist):
        pos = (pos + dirc) % 100
        if pos == 0:
            p2 += 1
    if pos == 0:
        p1 += 1

print(p1)
print(p2)
