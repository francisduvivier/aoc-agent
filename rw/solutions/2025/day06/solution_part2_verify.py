import sys
from itertools import groupby

def main():
    with open('input.txt', 'r') as f:
        lines = [line.rstrip('\n') for line in f]
    
    # Determine max width
    max_width = max(len(line) for line in lines)
    
    # Pad lines to same width
    lines = [line.ljust(max_width) for line in lines]
    
    # Group columns by whether they're all spaces
    columns = []
    for i in range(max_width):
        col = ''.join(line[i] for line in lines)
        columns.append(col)
    
    # Split into problems by empty column separators
    problems = []
    current = []
    for col in columns:
        if set(col) == {' '}:
            if current:
                problems.append(current)
                current = []
        else:
            current.append(col)
    if current:
        problems.append(current)
    
    # Process each problem right-to-left
    total = 0
    for problem in problems:
        # Reverse columns to read right-to-left
        reversed_cols = problem[::-1]
        
        # Extract operator (bottom of last column)
        op_line = reversed_cols[-1]
        operator = op_line[-1]
        
        # Extract numbers from each column
        nums = []
        for col in reversed_cols:
            # Remove trailing spaces and convert to int
            digits = col.rstrip(' ')
            if digits:
                nums.append(int(digits))
        
        # Calculate result
        if operator == '+':
            result = sum(nums)
        elif operator == '*':
            result = 1
            for n in nums:
                result *= n
        
        total += result
    
    print(total)

if __name__ == '__main__':
    main()
