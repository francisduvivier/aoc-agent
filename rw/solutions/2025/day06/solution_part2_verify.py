import sys
from itertools import zip_longest

def main():
    try:
        with open('input.txt', 'r') as f:
            lines = [line.rstrip('\n') for line in f]
    except FileNotFoundError:
        print("input.txt not found")
        return

    if not lines:
        print(0)
        return

    # Separate problems by full columns of spaces
    problems = []
    current_problem = []
    for col_idx in range(len(lines[0])):
        col_chars = [line[col_idx] for line in lines]
        if all(c == ' ' for c in col_chars):
            if current_problem:
                problems.append(current_problem)
                current_problem = []
        else:
            current_problem.append(col_chars)
    if current_problem:
        problems.append(current_problem)

    total = 0
    for problem in problems:
        # Each column is a number, top to bottom most significant to least
        numbers = []
        for col in problem[:-1]:  # Exclude operator column
            num_str = ''.join(c for c in col if c != ' ')
            if num_str:
                numbers.append(int(num_str))
        
        # Last column contains the operator
        op_col = problem[-1]
        op = ''.join(c for c in op_col if c != ' ')
        if op == '+':
            result = sum(numbers)
        elif op == '*':
            result = 1
            for n in numbers:
                result *= n
        else:
            continue
            
        total += result
        
    print(total)

if __name__ == '__main__':
    main()
