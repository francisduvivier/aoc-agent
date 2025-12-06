import sys

def solve():
    try:
        with open('input.txt', 'r') as f:
            instructions = f.read().strip()
    except FileNotFoundError:
        print("input.txt not found")
        return

    santa_pos = (0, 0)
    robo_pos = (0, 0)
    visited = {santa_pos}
    
    for i, move in enumerate(instructions):
        if i % 2 == 0:  # Santa's turn
            x, y = santa_pos
        else:  # Robo-Santa's turn
            x, y = robo_pos
            
        if move == '^':
            y += 1
        elif move == 'v':
            y -= 1
        elif move == '>':
            x += 1
        elif move == '<':
            x -= 1
            
        new_pos = (x, y)
        visited.add(new_pos)
        
        if i % 2 == 0:
            santa_pos = new_pos
        else:
            robo_pos = new_pos
    
    print(len(visited))

if __name__ == '__main__':
    solve()
