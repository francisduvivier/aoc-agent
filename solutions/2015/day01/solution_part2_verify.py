import sys

def main():
    sample_input = "()())"
    sample_answer = 5
    
    with open('input.txt', 'r') as f:
        puzzle_input = f.read().strip()
    
    # Part 2 solution
    floor = 0
    position = 0
    for i, char in enumerate(puzzle_input, 1):
        if char == '(':
            floor += 1
        elif char == ')':
            floor -= 1
        
        if floor == -1:
            position = i
            break
    
    # Calculate sample result
    sample_floor = 0
    sample_position = 0
    for i, char in enumerate(sample_input, 1):
        if char == '(':
            sample_floor += 1
        elif char == ')':
            sample_floor -= 1
        
        if sample_floor == -1:
            sample_position = i
            break
    
    print(f"---- Sample Solution Part 2: {sample_position} ----")
    print(f"---- Final Solution Part 2: {position} ----")

if __name__ == "__main__":
    main()
