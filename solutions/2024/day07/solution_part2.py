def solve_part2(lines):
    total = 0
    for line in lines:
        if not line:
            continue
        parts = line.split(':')
        target = int(parts[0])
        nums = list(map(int, parts[1].split()))
        
        n = len(nums)
        stack = [(nums[0], 0)]
        found = False
        
        while stack:
            current, idx = stack.pop()
            if idx == n - 1:
                if current == target:
                    found = True
                    break
                continue
            
            next_num = nums[idx + 1]
            # Try addition
            stack.append((current + next_num, idx + 1))
            # Try multiplication
            stack.append((current * next_num, idx + 1))
            # Try concatenation
            concat = int(str(current) + str(next_num))
            stack.append((concat, idx + 1))
        
        if found:
            total += target
    return total

if __name__ == '__main__':
    sample_input = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""
    sample_answer = 11387

    sample_result = solve_part2(sample_input.strip().splitlines())
    print(f"---- Sample Solution Part 2: {sample_result} ----")

    with open('input.txt') as f:
        lines = [line.strip() for line in f]
    final_result = solve_part2(lines)
    print(f"---- Final Solution Part 2: {final_result} ----")
