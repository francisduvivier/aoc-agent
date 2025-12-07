with open('input.txt') as f:
    lines = [line.strip() for line in f if line.strip()]

if not lines:
    print(0)
    print(0)
    exit()

width = len(lines[0])
num = len(lines)

# Part 1
transposed = zip(*lines)
gamma_bits = ''.join('1' if sum(int(bit) for bit in col) > num // 2 else '0' for col in transposed)
epsilon_bits = ''.join('0' if b == '1' else '1' for b in gamma_bits)
part1 = int(gamma_bits, 2) * int(epsilon_bits, 2)

# Part 2
def get_rating(cands, oxygen):
    c = cands[:]
    for col in range(width):
        if len(c) <= 1:
            break
        ones = sum(int(s[col]) for s in c)
        half = len(c) / 2
        bit = '1' if (ones >= half) == oxygen else '0'
        c = [s for s in c if s[col] == bit]
    return c[0]

oxy = int(get_rating(lines, True), 2)
co2 = int(get_rating(lines, False), 2)
part2 = oxy * co2

print(part1)
print(part2)
