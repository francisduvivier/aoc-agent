masses = [int(line.strip()) for line in open('input.txt') if line.strip()]

def fuel_part1(m):
    return m // 3 - 2

part1 = sum(fuel_part1(m) for m in masses)

def fuel_part2(m):
    total = 0
    while m > 0:
        f = m // 3 - 2
        if f <= 0:
            break
        total += f
        m = f
    return total

part2 = sum(fuel_part2(m) for m in masses)

print(part1)
print(part2)
