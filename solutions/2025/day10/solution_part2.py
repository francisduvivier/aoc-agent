# Edit this file: implement solve_part2

import re
from collections import defaultdict

def min_cost_flow(source, sink, graph, flow_needed):
    INF = 10**18
    V = len(graph)
    h = [0] * V
    prevv = [0] * V
    preve = [0] * V
    
    def add_edge(fr, to, cap, cost):
        graph[fr][to] = [cap, cost, len(graph[to])]
        graph[to][fr] = [0, -cost, len(graph[fr]) - 1]
    
    # Build graph inside, but since graph is passed, assume it's set up with add_edge calls outside.
    # Wait, actually, in the function, we assume graph is already built with the format.
    
    total_cost = 0
    while flow_needed > 0:
        dist = [INF] * V
        dist[source] = 0
        import heapq
        que = [(0, source)]  # (cost, vertex)
        while que:
            p = heapq.heappop(que)
            v = p[1]
            if dist[v] < p[0]: continue
            for to, edge in graph[v].items():
                cap, cost, _ = edge
                if cap > 0 and dist[to] > dist[v] + cost + h[v] - h[to]:
                    dist[to] = dist[v] + cost + h[v] - h[to]
                    prevv[to] = v
                    preve[to] = to
                    heapq.heappush(que, (dist[to], to))
        if dist[sink] == INF:
            return -1  # Cannot send more flow
        for i in range(V):
            if dist[i] < INF:
                h[i] += dist[i]
        d = flow_needed
        v = sink
        while v != source:
            d = min(d, graph[prevv[v]][v][0])
            v = prevv[v]
        flow_needed -= d
        total_cost += d * h[sink]
        v = sink
        while v != source:
            graph[prevv[v]][v][0] -= d
            graph[v][prevv[v]][0] += d
            v = prevv[v]
    return total_cost

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
        m = len(buttons)
        n = len(targets)
        V = m + n + 2
        source = 0
        sink = V - 1
        graph = [defaultdict(list) for _ in range(V)]
        # source to buttons: cap inf, cost 1
        for i in range(1, m+1):
            graph[source][i] = [10**9, 1, None]
            graph[i][source] = [0, -1, None]
        # buttons to counters
        for i, btn in enumerate(buttons, 1):
            for c in btn:
                if c < n:
                    j = m + 1 + c
                    graph[i][j] = [10**9, 0, None]
                    graph[j][i] = [0, 0, None]
        # counters to sink: cap targets[c], cost 0
        for c in range(n):
            j = m + 1 + c
            graph[j][sink] = [targets[c], 0, None]
            graph[sink][j] = [0, 0, None]
        flow_needed = sum(targets)
        cost = min_cost_flow(source, sink, graph, flow_needed)
        total += cost
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
