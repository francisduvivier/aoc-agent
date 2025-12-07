from itertools import product

def solve_part2(lines):
    total = 0
    for line in lines:
        parts = line.split(':')
        test_value = int(parts[0])
        numbers = list(map(int, parts[1].split()))
        
        # Try all combinations of operators (+, *, ||)
        # For n numbers, we need n-1 operators
        n = len(numbers)
        if n == 1:
            if numbers[0] == test_value:
                total += test_value
            continue
            
        # Generate all possible operator combinations
        # 0 = +, 1 = *, 2 = ||
        for ops in product([0, 1, 2], repeat=n-1):
            result = numbers[0]
            valid = True
            
            for i, op in enumerate(ops):
                next_num = numbers[i+1]
                
                if op == 0:  # addition
                    result += next_num
                elif op == 1:  # multiplication
                    result *= next_num
                else:  # concatenation
                    # Convert to strings, concatenate, then back to int
                    result = int(str(result) + str(next_num))
                
                # Early termination if we exceed the target
                if result > test_value:
                    valid = False
                    break
            
            if valid and result == test_value:
                total += test_value
                break
                
    return total

# Sample data from the problem statement
samples = [
    ("""190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20""", 11387)
]

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part2(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 2: {sample_result} ----")

# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part2(lines)
print(f"---- Final result Part 2: {final_result} ----")
