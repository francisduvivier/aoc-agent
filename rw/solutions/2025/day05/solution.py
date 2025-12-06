import sys

def main():
    with open('input.txt', 'r') as f:
        content = f.read().strip()
    
    parts = content.split('\n\n')
    if len(parts) < 2:
        print("0")
        print("0")
        return
    
    ranges_text = parts[0].strip()
    ids_text = parts[1].strip()
    
    # Parse ranges
    ranges = []
    for line in ranges_text.split('\n'):
        if '-' in line:
            start, end = map(int, line.split('-'))
            ranges.append((start, end))
    
    # Part 1: Count fresh IDs
    fresh_count = 0
    for line in ids_text.split('\n'):
        if line.strip():
            id_val = int(line.strip())
            is_fresh = False
            for start, end in ranges:
                if start <= id_val <= end:
                    is_fresh = True
                    break
            if is_fresh:
                fresh_count += 1
    
    # Part 2: Count total fresh IDs in ranges
    # Merge overlapping ranges
    if not ranges:
        total_fresh = 0
    else:
        # Sort ranges by start
        ranges.sort()
        merged = []
        current_start, current_end = ranges[0]
        
        for start, end in ranges[1:]:
            if start <= current_end + 1:  # Can merge (adjacent ranges count as one)
                current_end = max(current_end, end)
            else:
                merged.append((current_start, current_end))
                current_start, current_end = start, end
        
        merged.append((current_start, current_end))
        
        total_fresh = sum(end - start + 1 for start, end in merged)
    
    print(fresh_count)
    print(total_fresh)

if __name__ == '__main__':
    main()
