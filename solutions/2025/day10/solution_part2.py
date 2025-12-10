# Edit this file: implement solve_part2

def solve_part2(lines):
    total_presses = 0
    for line in lines:
        # Extract the joltage requirements and button wiring schematics
        parts = line.split('{')
        joltage_str = parts[1].rstrip('}')
        joltage_reqs = list(map(int, joltage_str.split(',')))

        # Extract button wiring schematics - FIXED: properly parse the line
        # Split the line to get the part between [ and {, then extract parentheses
        bracket_part = line.split('[')[1].split('{')[0]
        button_parts = []
        # Find all parentheses groups
        start = 0
        while True:
            open_idx = bracket_part.find('(', start)
            if open_idx == -1:
                break
            close_idx = bracket_part.find(')', open_idx)
            if close_idx == -1:
                break
            button_str = bracket_part[open_idx+1:close_idx]
            button_parts.append(button_str)
            start = close_idx + 1

        buttons = []
        for part in button_parts:
            if part.strip():
                buttons.append(tuple(map(int, part.split(','))))

        # Solve using BFS to find minimal presses
        from collections import deque
        n = len(joltage_reqs)
        target = tuple(joltage_reqs)
        start = tuple([0] * n)

        queue = deque()
        queue.append((start, 0))
        visited = set()
        visited.add(start)

        found = False
        while queue and not found:
            current, presses = queue.popleft()
            if current == target:
                total_presses += presses
                found = True
                break
            for button in buttons:
                new_state = list(current)
                for idx in button:
                    new_state[idx] += 1
                new_state = tuple(new_state)
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, presses + 1))
    return total_presses

# Sample data
samples = [
    ("[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}", 10),
    ("[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}", 12),
    ("[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}", 11),
    ("[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}\n[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}\n[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}", 33)
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
