def solve_part1(lines):
    disk_map = lines[0].strip()
    
    # Parse the disk map into files and free spaces
    files = []
    free_spaces = []
    
    for i, length in enumerate(disk_map):
        length = int(length)
        if i % 2 == 0:
            # Even indices are files
            files.append((i // 2, length))
        else:
            # Odd indices are free spaces
            free_spaces.append(length)
    
    # Build the initial disk layout
    disk = []
    file_idx = 0
    free_idx = 0
    
    while file_idx < len(files) or free_idx < len(free_spaces):
        if file_idx < len(files):
            file_id, file_len = files[file_idx]
            disk.extend([file_id] * file_len)
            file_idx += 1
        if free_idx < len(free_spaces):
            free_len = free_spaces[free_idx]
            disk.extend(['.'] * free_len)
            free_idx += 1
    
    # Compact the disk by moving files from right to left
    left_free = 0
    right_file = len(disk) - 1
    
    while left_free < right_file:
        # Find the leftmost free space
        while left_free < len(disk) and disk[left_free] != '.':
            left_free += 1
        
        if left_free >= right_file:
            break
            
        # Find the rightmost file block
        while right_file >= 0 and disk[right_file] == '.':
            right_file -= 1
            
        if right_file <= left_free:
            break
            
        # Move the file block to the free space
        disk[left_free] = disk[right_file]
        disk[right_file] = '.'
        left_free += 1
        right_file -= 1
    
    # Calculate the checksum
    checksum = 0
    for i, block in enumerate(disk):
        if block != '.':
            checksum += i * block
    
    return checksum

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples.
samples = [
    ("2333133121414131402", 1928)
]  # TODO: fill with actual samples and expected results

for idx, (sample_input, expected_result) in enumerate(samples, start=1):
    sample_result = solve_part1(sample_input.strip().splitlines())
    assert sample_result == expected_result, f"Sample {idx} result {sample_result} does not match expected {expected_result}"
    print(f"---- Sample {idx} result Part 1: {sample_result} ----") # YOU MUST NOT change this output format

# Run on the real puzzle input
with open('input.txt') as f:
    lines = [line.strip() for line in f]
final_result = solve_part1(lines)
print(f"---- Final result Part 1: {final_result} ----") # YOU MUST NOT change this output format
