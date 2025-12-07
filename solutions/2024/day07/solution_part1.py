def solve_part1(lines):
    total = 0
    for line in lines:
        if not line.strip():
            continue
        parts = line.split(':')
        target = int(parts[0])
        numbers = list(map(int, parts[1].split()))
        
        if len(numbers) == 1:
            if numbers[0] == target:
                total += target
            continue
            
        stack = [(numbers[0], 1)]
        found = False
        
        while stack and not found:
            current, idx = stack.pop()
            if idx == len(numbers):
                if current == target:
                    total += target
                    found = True
                continue
            
            if not found:
                stack.append((current + numbers[idx], idx + 1))
            if not found:
                stack.append((current * numbers[idx], idx + 1))
                
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
    sample_answer = 3749

    sample_result = solve_part1(sample_input.strip().splitlines())
    print(f"---- Sample Solution Part 1: {sample_result} ----")

    with open('input.txt') as f:
        lines = [line.strip() for line in f]
    final_result = solve_part1(lines)
    print(f"---- Final Solution Part 1: {final_result} ----")
