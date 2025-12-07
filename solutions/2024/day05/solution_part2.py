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
            # Sort the update correctly using topological sort
            # Build a set of all pages in this update
            pages = set(update)
            
            # For each page, find which other pages must come before it in this update
            before_map = {}
            for page in pages:
                before_map[page] = set()
            
            for x, y in rules:
                if x in pages and y in pages:
                    before_map[y].add(x)
            
            # Sort using Kahn's algorithm
            sorted_update = []
            # Start with pages that have no dependencies
            available = [p for p in pages if len(before_map[p]) == 0]
            
            while available:
                # Take a page with no remaining dependencies
                page = available.pop()
                sorted_update.append(page)
                
                # Remove this page from all dependency lists
                for other in pages:
                    if page in before_map[other]:
                        before_map[other].remove(page)
                        # If this other page now has no dependencies, add it to available
                        if len(before_map[other]) == 0:
                            available.append(other)
            
            # Add middle page of the correctly sorted update
            n = len(sorted_update)
            total += sorted_update[n // 2]
    
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

