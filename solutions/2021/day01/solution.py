with open('input.txt') as f:
    depths = [int(line.strip()) for line in f if line.strip()]

# Part 1
count1 = sum(1 for i in range(1, len(depths)) if depths[i] > depths[i - 1])

# Part 2
count2 = sum(1 for i in range(1, len(depths) - 2)
             if depths[i] + depths[i + 1] + depths[i + 2] > depths[i - 1] + depths[i] + depths[i + 1])

print(count1)
print(count2)
