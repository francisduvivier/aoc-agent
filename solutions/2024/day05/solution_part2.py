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
    
    # Build rule map: for each page, which pages must come before it
    must_come_before = {}
    for x, y in rules:
        if y not in must_come_before:
            must_come_before[y] = set()
        must_come_before[y].add(x)
    
    total = 0
    
    for update in updates:
        # Check if update is correct
        incorrect = False
        for i, page in enumerate(update):
            if page in must_come_before:
                # Check that all pages that must come before 'page' are indeed before it
                required_before = must_come_before[page]
                actual_before = set(update[:i])
                if not required_before.issubset(actual_before):
                    incorrect = True
                    break
        
        if incorrect:
            # Sort the update correctly
            n = len(update)
            # Bubble sort with the rules
            for i in range(n):
                for j in range(n - 1):
                    a, b = update[j], update[j + 1]
                    # Check if b must come before a (which would be wrong)
                    if a in must_come_before and b in must_come_before[a]:
                        # Swap
                        update[j], update[j + 1] = update[j + 1], update[j]
            
            # Add middle page
            total += update[n // 2]
    
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
