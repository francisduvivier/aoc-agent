import re
from math import gcd

def solve_part2(lines):
    total_cost = 0
    for i in range(0, len(lines), 4):
        # Parse button A
        ax, ay = map(int, re.findall(r'X\+(\d+), Y\+(\d+)', lines[i])[0])
        # Parse button B
        bx, by = map(int, re.findall(r'X\+(\d+), Y\+(\d+)', lines[i+1])[0])
        # Parse prize with offset
        px, py = map(int, re.findall(r'X=(\d+), Y=(\d+)', lines[i+2])[0])
        px += 10000000000000
        py += 10000000000000
        
        # Solve system of equations:
        # a*ax + b*bx = px
        # a*ay + b*by = py
        # Using Cramer's rule
        det = ax * by - ay * bx
        if det == 0:
            continue
            
        det_a = px * by - py * bx
        det_b = ax * py - ay * px
        
        if det_a % det == 0 and det_b % det == 0:
            a = det_a // det
            b = det_b // det
            if a >= 0 and b >= 0:
                total_cost += a * 3 + b * 1
                
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
Prize: X=18641, Y=10279""", 875318608908)
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
