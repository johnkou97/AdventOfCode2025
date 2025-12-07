if __name__ == "__main__":
    import numpy as np

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