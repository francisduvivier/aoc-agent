import sys

def parse_input():
    with open('input.txt') as f:
        lines = f.readlines()
    
    # Remove trailing newlines and pad to equal length
    max_len = max(len(line.rstrip('\n')) for line in lines)
    grid = []
    for line in lines:
        line = line.rstrip('\n')
        if len(line) < max_len:
            line += ' ' * (max_len - len(line))
        grid.append(line)
    
    return grid

def split_into_columns(grid):
    # Find column boundaries by looking for full columns of spaces
    width = len(grid[0])
    height = len(grid)
    
    # Identify columns that are entirely spaces (separators)
    separator_cols = []
    for col in range(width):
        if all(grid[row][col] == ' ' for row in range(height)):
            separator_cols.append(col)
    
    # Split into groups of columns
    groups = []
    start = 0
    for sep in separator_cols:
        if sep > start:
            groups.append(list(range(start, sep)))
        start = sep + 1
    if start < width:
        groups.append(list(range(start, width)))
    
    return groups, grid

def extract_number(grid, cols):
    # Extract digits from the specified columns, top to bottom
    digits = []
    for col in cols:
        for row in range(len(grid)):
            char = grid[row][col]
            if char.isdigit():
                digits.append(char)
    return int(''.join(digits)) if digits else 0

def solve():
    grid = parse_input()
    groups, grid = split_into_columns(grid)
    
    total = 0
    
    # Process groups from right to left
    for group_cols in reversed(groups):
        # Find the operator at the bottom of this group
        operator_row = len(grid) - 1
        while operator_row >= 0 and not grid[operator_row][group_cols[0]] in '+*':
            operator_row -= 1
        
        if operator_row < 0:
            continue
            
        operator = grid[operator_row][group_cols[0]]
        
        # Split this group into sub-columns for each number
        # Find spaces within this group that separate numbers
        subgroups = []
        current_subgroup = []
        
        for col in group_cols:
            if grid[operator_row][col] == ' ':
                if current_subgroup:
                    subgroups.append(current_subgroup)
                    current_subgroup = []
            else:
                current_subgroup.append(col)
        
        if current_subgroup:
            subgroups.append(current_subgroup)
        
        # Extract numbers from each subgroup
        numbers = []
        for subgroup in subgroups:
            numbers.append(extract_number(grid, subgroup))
        
        # Apply the operation
        if operator == '+':
            result = sum(numbers)
        elif operator == '*':
            result = 1
            for num in numbers:
                result *= num
        
        total += result
    
    print(total)

if __name__ == '__main__':
    solve()
