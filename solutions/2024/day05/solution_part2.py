def solve_part2(lines):
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
    
    # Build a set of valid orderings for quick lookup
    valid_order = set(rules)
    
    def is_correct(update):
        # Check if update respects all relevant rules
        for i in range(len(update)):
            for j in range(i + 1, len(update)):
                if (update[i], update[j]) not in valid_order:
                    return False
        return True
    
    def fix_update(update):
        # Bubble sort using the rules
        fixed = update[:]
        n = len(fixed)
        for i in range(n):
            for j in range(n - 1):
                # If (fixed[j], fixed[j+1]) is not a valid rule,
                # we need to swap them
                if (fixed[j], fixed[j+1]) not in valid_order:
                    # Find if the reverse is a valid rule
                    if (fixed[j+1], fixed[j]) in valid_order:
                        fixed[j], fixed[j+1] = fixed[j+1], fixed[j]
        return fixed
    
    total = 0
    for update in updates:
        if not is_correct(update):
            fixed = fix_update(update)
            total += fixed[len(fixed) // 2]
    
    return total

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples.
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
97,13,75,29,47""", 123)
]  # TODO: fill with actual samples and expected results

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part2(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 2: {sample_result} ----") # YOU MUST NOT change this output format

# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part2(lines)
print(f"---- Final result Part 2: {final_result} ----") # YOU MUST NOT change this output format
