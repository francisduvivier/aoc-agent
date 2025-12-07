def solve_part1(lines):
    from collections import defaultdict
    
    antennas = defaultdict(list)
    rows = len(lines)
    cols = len(lines[0]) if rows > 0 else 0
    
    for i in range(rows):
        for j in range(cols):
            char = lines[i][j]
            if char != '.':
                antennas[char].append((i, j))
    
    antinodes = set()
    
    for freq, positions in antennas.items():
        n = len(positions)
        for i in range(n):
            x1, y1 = positions[i]
            for j in range(i + 1, n):
                x2, y2 = positions[j]
                dx = x2 - x1
                dy = y2 - y1
                
                antinode1 = (x1 - dx, y1 - dy)
                antinode2 = (x2 + dx, y2 + dy)
                
                if 0 <= antinode1[0] < rows and 0 <= antinode1[1] < cols:
                    antinodes.add(antinode1)
                if 0 <= antinode2[0] < rows and 0 <= antinode2[1] < cols:
                    antinodes.add(antinode2)
    
    return len(antinodes)

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
    sample_answer = 14

    sample_result = solve_part1(sample_input.strip().splitlines())
    print(f"---- Sample Solution Part 1: {sample_result} ----")

    with open('input.txt') as f:
        lines = [line.strip() for line in f]
    final_result = solve_part1(lines)
    print(f"---- Final Solution Part 1: {final_result} ----")
