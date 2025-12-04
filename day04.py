def remove_rolls(diagram: list[list[int]]) -> tuple[list[list[int]], int]:
    """
    Remove rolls from the diagram.
    A roll can be removed if it is surrounded by fewer than 4 other rolls.
    Returns the updated diagram and the count of removed rolls.
    """

    movable = []
    
    # top row
    for j in range(1, len(diagram[0])-1):
        total = (diagram[0][j-1] + diagram[0][j+1] +
                 diagram[1][j-1] + diagram[1][j] + diagram[1][j+1])
        if diagram[0][j] == 1 and total < 4:
            movable.append((0, j))
    
    # bottom row
    for j in range(1, len(diagram[0])-1):
        total = (diagram[-2][j-1] + diagram[-2][j] + diagram[-2][j+1] +
                 diagram[-1][j-1] + diagram[-1][j+1])
        if diagram[-1][j] == 1 and total < 4:
            movable.append((len(diagram)-1, j))
    
    # left column
    for i in range(1, len(diagram)-1):
        total = (diagram[i-1][0] + diagram[i-1][1] +
                 diagram[i][1] +
                 diagram[i+1][0] + diagram[i+1][1])
        if diagram[i][0] == 1 and total < 4:
            movable.append((i, 0))
    
    # right column
    for i in range(1, len(diagram)-1):
        total = (diagram[i-1][-2] + diagram[i-1][-1] +
                 diagram[i][-2] +
                 diagram[i+1][-2] + diagram[i+1][-1])
        if diagram[i][-1] == 1 and total < 4:
            movable.append((i, len(diagram[0])-1))

   #  top-left corner
    total = diagram[0][1] + diagram[1][0] + diagram[1][1]
    if diagram[0][0] == 1 and total < 4:
        movable.append((0, 0))
    
    # top-right corner
    total = diagram[0][-2] + diagram[1][-2] + diagram[1][-1]
    if diagram[0][-1] == 1 and total < 4:
        movable.append((0, len(diagram[0])-1))
    
    # bottom-left corner
    total = diagram[-2][0] + diagram[-2][1] + diagram[-1][1]
    if diagram[-1][0] == 1 and total < 4:
        movable.append((len(diagram)-1, 0))
    
    # bottom-right corner
    total = diagram[-2][-2] + diagram[-2][-1] + diagram[-1][-2]
    if diagram[-1][-1] == 1 and total < 4:
        movable.append((len(diagram)-1, len(diagram[0])-1))
    
    # inner cells
    for i in range(1, len(diagram)-1):
        for j in range(1, len(diagram[0])-1):
            if diagram[i][j] == 1:
                total = (diagram[i-1][j-1] + diagram[i-1][j] + diagram[i-1][j+1] +
                        diagram[i][j-1]                 + diagram[i][j+1] +
                        diagram[i+1][j-1] + diagram[i+1][j] + diagram[i+1][j+1])
                if total < 4:
                    movable.append((i, j))

    for position in movable:
        i, j = position
        diagram[i][j] = 0

    return diagram, len(movable)


if __name__ == "__main__":
    diagram = []
    with open("inputs/day4.txt") as file:
        for line in file:
            diagram.append(line.strip())

    new_diagram = []
    for row in diagram:
        new_row = [1 if char == "@" else 0 for char in row]
        new_diagram.append(new_row)

    removed_count = 1
    repetitions = 0
    total_removed = 0

    # Part 2: How many rolls of paper can be removed in total?
    while removed_count > 0:
        new_diagram, removed_count = remove_rolls(new_diagram)
        total_removed += removed_count
        repetitions += 1

        # Part 1: How many rolls of paper can be accessed by the forklift
        if repetitions == 1:
            removable = removed_count

    print("Removable Rolls:", removable)
    print("Total Rolls Removed:", total_removed)