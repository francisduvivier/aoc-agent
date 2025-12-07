def largest_subseq(s, k):
    n = len(s)
    m = n - k
    stack = []
    for c in s:
        while stack and stack[-1] < c and m > 0:
            stack.pop()
            m -= 1
        stack.append(c)
    while m > 0:
        stack.pop()
        m -= 1
    return ''.join(stack)

with open('input.txt') as f:
    lines = [line.strip() for line in f if line.strip()]

part1 = 0
part2 = 0
for s in lines:
    num1 = int(largest_subseq(s, 2))
    part1 += num1
    num2 = int(largest_subseq(s, 12))
    part2 += num2

print(part1)
print(part2)
