with open('input.txt') as f:
    line = f.read().strip()
ranges_str = line.split(',')
sum1 = 0
sum2 = 0
for r in ranges_str:
    start, end = map(int, r.split('-'))
    for i in range(start, end + 1):
        s = str(i)
        n = len(s)
        # Part 1
        if n % 2 == 0:
            half = n // 2
            if s[:half] == s[half:]:
                sum1 += i
        # Part 2
        is_invalid = False
        for d in range(1, n // 2 + 1):
            if n % d == 0:
                seq = s[:d]
                match = True
                for j in range(d, n, d):
                    if s[j:j + d] != seq:
                        match = False
                        break
                if match:
                    is_invalid = True
                    break
        if is_invalid:
            sum2 += i
print(sum1)
print(sum2)
