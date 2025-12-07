from collections import defaultdict

def solve_part2(lines):
    grid = [list(line) for line in lines]
    rows, cols = len(grid), len(grid[0])
    
    # Group antennas by frequency
    antennas = defaultdict(list)
    for r in range(rows):
        for c in range(cols):
            char = grid[r][c]
            if char != '.':
                antennas[char].append((r, c))
    
    antinodes = set()
    
    # For each frequency, find all antinodes
    for freq, points in antennas.items():
        n = len(points)
        if n < 2:
            continue
            
        # All antennas of this frequency are antinodes
        antinodes.update(points)
        
        # Check all pairs of antennas
        for i in range(n):
            for j in range(i + 1, n):
                r1, c1 = points[i]
                r2, c2 = points[j]
                
                dr = r2 - r1
                dc = c2 - c1
                
                # Find all points on the line between and beyond the two antennas
                # Using gcd to get the step in reduced form
                gcd_val = abs(dr)
                if dc != 0:
                    gcd_val = gcd(gcd_val, abs(dc))
                if gcd_val == 0:
                    continue
                    
                step_r = dr // gcd_val
                step_c = dc // gcd_val
                
                # Extend in both directions
                r, c = r1, c1
                while 0 <= r < rows and 0 <= c < cols:
                    antinodes.add((r, c))
                    r += step_r
                    c += step_c
                
                r, c = r1, c1
                while 0 <= r < rows and 0 <= c < cols:
                    antinodes.add((r, c))
                    r -= step_r
                    c -= step_c
    
    return len(antinodes)

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

if __name__ == '__main__':
    sample_input = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""
    sample_answer = 34

    sample_result = solve_part2(sample_input.strip().splitlines())
    print(f"---- Sample Solution Part 2: {sample_result} ----")

    with open('input.txt') as f:
        lines = [line.strip() for line in f]
    final_result = solve_part2(lines)
    print(f"---- Final Solution Part 2: {final_result} ----")
