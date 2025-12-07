import re
from math import gcd

def solve_part2(lines):
    total_cost = 0
    for i in range(0, len(lines), 4):
        a_line = lines[i]
        b_line = lines[i+1]
        prize_line = lines[i+2]
        
        ax = int(re.search(r'X\+(\d+)', a_line).group(1))
        ay = int(re.search(r'Y\+(\d+)', a_line).group(1))
        bx = int(re.search(r'X\+(\d+)', b_line).group(1))
        by = int(re.search(r'Y\+(\d+)', b_line).group(1))
        px = int(re.search(r'X=(\d+)', prize_line).group(1)) + 10000000000000
        py = int(re.search(r'Y=(\d+)', prize_line).group(1)) + 10000000000000
        
        # Solve system: a*ax + b*bx = px, a*ay + b*by = py
        # Using Cramer's rule
        det = ax * by - ay * bx
        if det == 0:
            continue
            
        # Use exact integer arithmetic to avoid floating point errors
        a_numer = px * by - py * bx
        b_numer = ax * py - ay * px
        
        if a_numer % det == 0 and b_numer % det == 0:
            a_presses = a_numer // det
            b_presses = b_numer // det
            if a_presses >= 0 and b_presses >= 0:
                total_cost += a_presses * 3 + b_presses
            
    return total_cost

# Sample data from the problem statement
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
Prize: X=18641, Y=10279""", 87384170492566)
]

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part2(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 2: {sample_result} ----")

with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part2(lines)
print(f"---- Final result Part 2: {final_result} ----")
