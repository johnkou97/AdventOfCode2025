if __name__ == "__main__":
    instructions = []
    with open("inputs/day1.txt") as file:
        for line in file:
            instructions.append(line.strip())

    starting_position = 50
    position = starting_position
    number_of_0s = 0
    total_rotations = 0
    
    for instruction in instructions:
        direction = instruction[0]
        steps = int(instruction[1:])

        if direction == 'R':
            new_position = position + steps
        elif direction == 'L':
            new_position = position - steps
        
        # Part 1: Count how many times the dial is left pointing at 0 after any rotation in the sequence.
        if new_position % 100 == 0:
            number_of_0s += 1

        # Part 2: Count how many times the dial crosses the 0 position.
        if direction == "R":
            gap = 100 - position
            if steps >= gap:
                total_rotations += 1 + (steps - gap) // 100
        elif direction == "L":
            gap = position
            if gap == 0:
                gap = 100   # Adjust for full rotation when at 0
            if steps >= gap:
                total_rotations += 1 + (steps - gap) // 100

        position = new_position % 100

    print(f"Password of the door: {number_of_0s}")
    print(f"Password of the door with method 0x434C49434B: {total_rotations}")