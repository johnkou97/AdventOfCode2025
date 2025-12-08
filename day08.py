if __name__ == "__main__":
    import numpy as np

    positions = []
    with open("inputs/day8.txt") as file:
        for line in file:
            positions.append([int(x) for x in line.strip().split(",")])
    positions = np.array(positions)

    distance_matrix = np.linalg.norm(positions[:, np.newaxis] - positions, axis=2)
    distance_matrix[np.tril_indices_from(distance_matrix)] = np.inf


    circuits = []
    i = 0
    while True:
        # Part 1: Multiply the sizes of the three largest circuits after 1000 connections
        if i == 1000:
            snapshot_circuits = circuits.copy()

        min_dist = np.min(distance_matrix)
        min_indices = np.unravel_index(np.argmin(distance_matrix), distance_matrix.shape)
        
        if any(min_indices[0] in list(circuit) for circuit in circuits):
                        # check if the other index is also in a circuit
            if any(min_indices[1] in list(circuit) for circuit in circuits):
                        # if they in the same circuit, skip
                if any(min_indices[0] in list(circuit) and min_indices[1] in list(circuit) for circuit in circuits):
                    distance_matrix[min_indices] = np.inf
                    continue
                else:   # if they are in different circuits, merge them
                    circuit1 = next(list(circuit) for circuit in circuits if min_indices[0] in list(circuit))
                    circuit2 = next(list(circuit) for circuit in circuits if min_indices[1] in list(circuit))
                    circuits.remove(circuit1)
                    circuits.remove(circuit2)
                    circuits.append(list(set(circuit1) | set(circuit2)))
            else:       # only min_indices[0] is in a circuit
                        # add min_indices[1] to that circuit
                for idx, circuit in enumerate(circuits):
                    if min_indices[0] in circuit:
                        new_circuit = list(circuit) + [min_indices[1]]
                        circuits[idx] = list(new_circuit)
                        i += 1
                        break
        elif any(min_indices[1] in list(circuit) for circuit in circuits):
                        # only min_indices[1] is in a circuit
                        # add min_indices[0] to that circuit
            for idx, circuit in enumerate(circuits):
                if min_indices[1] in list(circuit):
                    new_circuit = list(circuit) + [min_indices[0]]
                    circuits[idx] = list(new_circuit)
                    i += 1   
                    break
        else:           # neither index is in a circuit
                        # create a new circuit
            circuits.append([min_indices[0], min_indices[1]])
        
        distance_matrix[min_indices] = np.inf

        # Part 2: Multiply the X coordinates of the last two junction points we need to connect
        if sum(len(circuit) for circuit in circuits) == len(positions):
            if len(circuits) == 1:
                x_coords = (positions[min_indices[0]][0], positions[min_indices[1]][0])
                break

        i += 1

    circuit_lengths = [len(circuit) for circuit in snapshot_circuits]
    circuit_lengths.sort(reverse=True)
    multiplier = circuit_lengths[0] * circuit_lengths[1] * circuit_lengths[2]

    print(f"Multiply the sizes of the three largest circuits after 1000 connections: {multiplier}")
    print(f"Multiply the X coordinates of the last two junction points we need to connect: {x_coords[0]*x_coords[1]}")