# Edit this file: implement solve_part2

def solve_part2(lines):
    total_presses = 0
    for line in lines:
        # Extract the joltage requirements and button wiring schematics
        parts = line.split('{')
        joltage_str = parts[1].rstrip('}')
        joltage_reqs = list(map(int, joltage_str.split(',')))

        # Extract button wiring schematics
        bracket_part = line.split('[')[1].split('{')[0]
        button_parts = []
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

        # Convert buttons to a matrix where each row represents a button
        # and each column represents a counter
        n = len(joltage_reqs)
        m = len(buttons)
        matrix = [[0]*m for _ in range(n)]
        for j in range(m):
            for i in buttons[j]:
                matrix[i][j] = 1

        # Solve the system of equations using a greedy approach
        # We'll try to find the minimal number of presses by considering
        # the buttons that cover the most remaining requirements first
        presses = [0] * m
        remaining = joltage_reqs.copy()

        while any(remaining):
            # Find the button that covers the most remaining requirements
            best_button = -1
            best_score = -1
            for j in range(m):
                score = sum(matrix[i][j] for i in range(n) if remaining[i] > 0)
                if score > best_score:
                    best_score = score
                    best_button = j
            if best_button == -1:
                break  # No button can help, which shouldn't happen per problem statement
            presses[best_button] += 1
            for i in range(n):
                if matrix[i][best_button]:
                    remaining[i] -= 1

        total_presses += sum(presses)
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
