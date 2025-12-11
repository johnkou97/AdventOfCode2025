from functools import lru_cache

@lru_cache(maxsize=None)
def count_paths(start, end, flag_dac=False, flag_fft=False):
    """
    Recursive function to count paths from start to end.
    Also counts paths that pass through 'dac' and 'fft'.
    """
    if start == end:
        return 1, 1 if (flag_dac and flag_fft) else 0
    
    if start == 'dac':
        flag_dac = True
    if start == 'fft':
        flag_fft = True

    next_steps = tuple(outs[devices.index(start)])
    total = 0
    total_with_flags = 0
    for step in next_steps:
        paths, flags = count_paths(step, end, flag_dac, flag_fft)
        total += paths
        total_with_flags += flags
    return total, total_with_flags

if __name__ == "__main__":
    devices = []
    outs = []
    with open("inputs/day11.txt") as file:
        for line in file:
            devices.append(line.strip().split(': ')[0])
            outs.append(line.strip().split(': ')[1].split(' '))
    
    # Part 1: Count paths from "you" to "out"
    total_paths, _ = count_paths("you", "out")
    print(f"Total paths from YOU to OUT: {total_paths}")

    # Part 2: Count paths from "svr" to "out" that visit "dac" and "fft"
    total_paths, total_with_flags = count_paths("svr", "out", False, False)
    print(f"Total paths from SVR to OUT passing through DAC and FFT: {total_with_flags}")