def solve_part1(lines):
    # Split rules and updates
    rules = []
    updates = []
    parsing_rules = True
    
    for line in lines:
        if line == "":
            parsing_rules = False
            continue
        if parsing_rules:
            x, y = map(int, line.split("|"))
            rules.append((x, y))
        else:
            updates.append(list(map(int, line.split(","))))
    
    # Build a set of valid orderings
    valid_orders = set(rules)
    
    total = 0
    for update in updates:
        # Check if update is in correct order
        correct = True
        for i in range(len(update)):
            for j in range(i + 1, len(update)):
                if (update[i], update[j]) not in valid_orders:
                    correct = False
                    break
            if not correct:
                break
        
        if correct:
            # Add middle page number
            total += update[len(update) // 2]
    
    return total

# Sample data from problem statement
samples = [
    ("""47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47""", 143)
]

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part1(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 1: {sample_result} ----")

# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part1(lines)
print(f"---- Final result Part 1: {final_result} ----")
