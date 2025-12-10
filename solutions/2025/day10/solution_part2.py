# Edit this file: implement solve_part2

import re
from collections import deque
import heapq  # Added for priority queue to implement A* search

def solve_part2(lines):
    total = 0
    for line in lines:
        button_matches = re.findall(r'\(([^)]+)\)', line)
        target_match = re.search(r'\{([^}]+)\}', line)
        if not target_match:
            continue
        targets = list(map(int, target_match.group(1).split(',')))
        buttons = []
        for bm in button_matches:
            btn = tuple(map(int, bm.split(',')))
            buttons.append(btn)
        n = len(targets)
        start = tuple([0] * n)
        goal = tuple(targets)
        # A* search to find min presses, with heuristic sum of remaining increments
        # Priority queue: (priority, presses, state)
        pq = []
        heapq.heappush(pq, (0, 0, start))  # heuristic for start is sum(targets)
        visited = set([start])
        min_presses = -1
        while pq:
            _, presses, current = heapq.heappop(pq)
            if current == goal:
                min_presses = presses
                break
            for btn in buttons:
                new_state = list(current)
                for c in btn:
                    if c < n:
                        new_state[c] += 1
                new_state = tuple(new_state)
                # Pruning: skip if any counter exceeds its target
                if any(new_state[c] > targets[c] for c in range(n)):
                    continue
                if new_state not in visited:
                    visited.add(new_state)
                    # Heuristic: sum of remaining increments for each counter
                    h = sum(targets[c] - new_state[c] for c in range(n))
                    heapq.heappush(pq, (presses + 1 + h, presses + 1, new_state))
        if min_presses != -1:
            total += min_presses
    return total

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples IF there are any samples given for part 2.
samples = [
    ("[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}\n[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}\n[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}", 33)
]

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part2(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 2: {sample_result} ----") # YOU MUST NOT change this output format
# print(f"---- Sample NONE result Part 2: NONE ----") # Uncomment this if no samples are given for part 2
# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part2(lines)
print(f"---- Final result Part 2: {final_result} ----") # YOU MUST NOT change this output format
