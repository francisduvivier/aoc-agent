# Edit this file: implement solve_part2

def solve_part2(lines):
    total_presses = 0
    for line in lines:
        # Extract the joltage requirements and button wiring schematics
        parts = line.split('{')
        joltage_str = parts[1].rstrip('}')
        joltage_reqs = list(map(int, joltage_str.split(',')))

        # Extract button wiring schematics
        button_parts = parts[0].split('[')[1].split(')')[0].split('(')
        button_parts = [part.strip() for part in button_parts if part.strip()]
        buttons = []
        for part in button_parts:
            if part.startswith('['):
                part = part[1:]
            if part.endswith(')'):
                part = part[:-1]
            if part:
                buttons.append(tuple(map(int, part.split(','))))

        # Solve the system of equations to find the minimum button presses
        # We need to find non-negative integers x_i such that sum(x_i * button_i) = joltage_reqs
        # This is a linear Diophantine system. We'll use a greedy approach to find the minimal solution.
        # Since the problem is small, we can use a BFS approach to find the minimal solution.

        from collections import deque
        n = len(joltage_reqs)
        m = len(buttons)

        # We'll represent the state as a tuple of current joltage levels
        start = tuple([0] * n)
        target = tuple(joltage_reqs)

        # BFS setup
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
        if not found:
            # If BFS didn't find a solution, try a different approach (though problem states it's solvable)
            # This is a fallback, but the problem guarantees a solution exists
            pass
    return total_presses

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples IF there are any samples given for part 2.
samples = [
    ("[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}", 10),
    ("[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}", 12),
    ("[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}", 11),
    ("[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}\n[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}\n[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}", 33)
]

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part2(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 2: {sample_result} ----") # YOU MUST NOT change this output format
# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part2(lines)
print(f"---- Final result Part 2: {final_result} ----") # YOU MUST NOT change this output format
