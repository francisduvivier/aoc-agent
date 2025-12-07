import re

def solve_part1(lines):
    total_cost = 0
    i = 0
    while i < len(lines):
        if not lines[i].startswith('Button A'):
            i += 1
            continue
        
        # Parse Button A
        ax, ay = map(int, re.findall(r'X\+(\d+), Y\+(\d+)', lines[i])[0])
        i += 1
        
        # Parse Button B
        bx, by = map(int, re.findall(r'X\+(\d+), Y\+(\d+)', lines[i])[0])
        i += 1
        
        # Parse Prize
        px, py = map(int, re.findall(r'X=(\d+), Y=(\d+)', lines[i])[0])
        i += 1
        
        # Solve for presses of A and B
        # ax * a + bx * b = px
        # ay * a + by * b = py
        
        # Using elimination:
        # a = (px * by - py * bx) / (ax * by - ay * bx)
        # b = (px - ax * a) / bx (if bx != 0) or (py - ay * a) / by
        
        denominator = ax * by - ay * bx
        if denominator == 0:
            continue
            
        a_presses = (px * by - py * bx) / denominator
        if bx != 0:
            b_presses = (px - ax * a_presses) / bx
        else:
            b_presses = (py - ay * a_presses) / by
            
        # Check if both are integers and within valid range
        if a_presses == int(a_presses) and b_presses == int(b_presses):
            a_presses = int(a_presses)
            b_presses = int(b_presses)
            if 0 <= a_presses <= 100 and 0 <= b_presses <= 100:
                total_cost += a_presses * 3 + b_presses * 1
                
    return total_cost

# Sample data
samples = [
("""Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279""", 480)
]

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part1(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 1: {sample_result} ----")

with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part1(lines)
print(f"---- Final result Part 1: {final_result} ----")
