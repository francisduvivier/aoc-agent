def main():
    sample_input = "2x3x4\n1x1x10"
    sample_answer = 48  # 34 + 14 = 48

    total_ribbon = 0
    with open('input.txt', 'r') as f:
        for line in f:
            l, w, h = map(int, line.strip().split('x'))
            sides = sorted([l, w, h])
            wrap = 2 * (sides[0] + sides[1])
            bow = l * w * h
            total_ribbon += wrap + bow

    sample_lines = sample_input.strip().split('\n')
    sample_total = 0
    for line in sample_lines:
        l, w, h = map(int, line.split('x'))
        sides = sorted([l, w, h])
        wrap = 2 * (sides[0] + sides[1])
        bow = l * w * h
        sample_total += wrap + bow

    print(f"---- Sample Solution Part 2: {sample_total} ----")
    print(f"---- Final Solution Part 2: {total_ribbon} ----")

if __name__ == "__main__":
    main()
