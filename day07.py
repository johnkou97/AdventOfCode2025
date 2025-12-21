if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--visualize', '-v', action='store_true')
    args = parser.parse_args()

    maze = []
    with open("inputs/day7.txt") as file:
        for line in file:
            maze.append(list(line.strip()))
    maze = np.array(maze)

    start = np.where(maze == "S")
    start = (int(start[0][0]), int(start[1][0]))
    end_length = len(maze) - 1
    i = 0
    traces = [start[1]]
    split_counter = 0
    trace_tracker = np.zeros((len(maze), len(maze[0])), dtype=int)
    trace_tracker[start] = 1


    # Part 1: Count the number of splits for a tachyon beam.
    # Part 2: How many different timelines would a tachyon beam end up on?
    while i < end_length:
        new_traces = []
        for trace in traces:
            if maze[i+1, trace] == '^':
                split_counter += 1
                new_traces.append(trace - 1)
                new_traces.append(trace + 1)
                trace_tracker[i+1, trace - 1] += trace_tracker[i, trace]
                trace_tracker[i+1, trace + 1] += trace_tracker[i, trace]
            else:   # maze[i+1, trace] == '.'
                new_traces.append(trace)
                trace_tracker[i+1, trace] += trace_tracker[i, trace]
        traces = list(set(new_traces))
        i += 1

    print(f"Number of splits for the tachyon beam: {split_counter}")
    print(f"Number of timelines the tachyon beam ends up on: {sum(trace_tracker[end_length, :])}")

    if args.visualize:
        import os
        os.makedirs('visualizations', exist_ok=True)

        plt.figure(figsize=(12, 10))
        plt.gca().set_facecolor('black')
        
        beam_intensity = np.log1p(trace_tracker)
        cmap = plt.get_cmap('inferno')

        im = plt.imshow(beam_intensity, cmap=cmap, aspect='auto', interpolation='bilinear')
        
        plt.scatter(start[1], start[0], c='lime', marker='*', s=300, label='Start', edgecolors='white', linewidths=1.5)

        split_rows, split_cols = np.where(maze == '^')
        plt.scatter(split_cols, split_rows, c='red', marker='x', s=20, alpha=0.7, label='Split points')
        
        plt.title('Tachyon Beam Intensity Map', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Column Position', fontsize=12)
        plt.ylabel('Row Position', fontsize=12)
        plt.legend(loc='upper right', fontsize=10)
        cbar = plt.colorbar(im, label='log(Count + 1)')
        cbar.ax.tick_params(labelsize=10)
        plt.ylim(len(maze) - 1, -10)
        
        plt.tight_layout()
        plt.savefig('visualizations/day07_tree.png', dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()