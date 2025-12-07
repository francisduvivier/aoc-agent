import sys

def main():
    total_ribbon = 0
    try:
        with open('input.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    l, w, h = map(int, line.split('x'))
                    # Calculate volume for bow
                    bow = l * w * h
                    
                    # Calculate smallest perimeter
                    perimeters = [
                        2 * (l + w),
                        2 * (w + h),
                        2 * (h + l)
                    ]
                    ribbon = min(perimeters)
                    
                    total_ribbon += ribbon + bow
                except (ValueError, IndexError):
                    print(f"Invalid line format: {line}", file=sys.stderr)
                    continue
    except FileNotFoundError:
        print("input.txt not found", file=sys.stderr)
        return
    
    print(total_ribbon)

if __name__ == "__main__":
    main()
