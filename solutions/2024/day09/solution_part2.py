def solve_part2(lines):
    disk_map = lines[0].strip()
    
    # Parse the disk map into files and free spaces
    files = []
    free_spaces = []
    file_id = 0
    
    for i, length in enumerate(map(int, disk_map)):
        if i % 2 == 0:
            # File
            files.append((file_id, length))
            file_id += 1
        else:
            # Free space
            free_spaces.append(length)
    
    # Build the initial disk layout
    disk = []
    file_iter = iter(files)
    free_iter = iter(free_spaces)
    
    for i, length in enumerate(map(int, disk_map)):
        if i % 2 == 0:
            # Add file blocks
            file_id, file_len = next(file_iter)
            disk.extend([file_id] * file_len)
        else:
            # Add free space
            free_len = next(free_iter)
            disk.extend([-1] * free_len)
    
    # Move files from highest ID to lowest
    # For each file, find the leftmost free space that can fit it
    for file_id in range(len(files) - 1, -1, -1):
        file_len = files[file_id][1]
        
        # Find the position of this file
        file_start = -1
        file_end = -1
        consecutive_count = 0
        
        for i, block in enumerate(disk):
            if block == file_id:
                if file_start == -1:
                    file_start = i
                file_end = i
                consecutive_count += 1
            elif block != file_id and consecutive_count > 0:
                break
        
        if consecutive_count != file_len:
            # Find the actual file
            file_start = -1
            consecutive_count = 0
            for i, block in enumerate(disk):
                if block == file_id:
                    if consecutive_count == 0:
                        file_start = i
                    consecutive_count += 1
                    file_end = i
                elif consecutive_count > 0:
                    if consecutive_count == file_len:
                        break
                    consecutive_count = 0
                    file_start = -1
    
        # Look for leftmost free space that can fit this file
        best_pos = -1
        best_consecutive = 0
        current_consecutive = 0
        
        for i in range(file_start):
            if disk[i] == -1:
                current_consecutive += 1
                if current_consecutive >= file_len:
                    best_pos = i - file_len + 1
                    break
            else:
                current_consecutive = 0
        
        # Move the file if we found a suitable position
        if best_pos != -1:
            # Clear the original file position
            for i in range(file_start, file_start + file_len):
                disk[i] = -1
            # Place the file in the new position
            for i in range(best_pos, best_pos + file_len):
                disk[i] = file_id
    
    # Calculate checksum
    checksum = 0
    for i, block in enumerate(disk):
        if block != -1:
            checksum += i * block
    
    return checksum

# Sample data – may contain multiple samples from the problem statement.
# Populate this list with (sample_input, expected_result) tuples.
samples = [
    ("2333133121414131402", 2858)
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
