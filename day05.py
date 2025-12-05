if __name__ == "__main__":
    ranges = []
    ingredients = []
    with open("inputs/day5.txt") as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if not line.strip():
                break
            ranges.append(tuple(map(int, line.strip().split("-"))))

        for j in range(i + 1, len(lines)):
            ingredients.append(int(lines[j].strip()))

    fresh_low = [r[0] for r in ranges]
    fresh_high = [r[1] for r in ranges]

    # Part 1: How many ingredients are fresh
    fresh_ingredients = []
    for ingredient in ingredients:
        if any(low <= ingredient <= high for low, high in zip(fresh_low, fresh_high)):
            fresh_ingredients.append(ingredient)

    print("Total Fresh Ingredients:", len(fresh_ingredients))

    # Part 2: How many IDs are considered fresh
    sorted_ranges = sorted(zip(fresh_low, fresh_high), key=lambda x: x[0])
    fresh_low, fresh_high = zip(*sorted_ranges)

    ranges_no_overlap = [[fresh_low[0], fresh_high[0]]]
    j = 0
    for i in range(1, len(fresh_low)):
        if fresh_low[i] <= ranges_no_overlap[j][1]:
            ranges_no_overlap[j][1] = max(ranges_no_overlap[j][1], fresh_high[i])
        else:
            ranges_no_overlap.append([fresh_low[i], fresh_high[i]])
            j += 1

    total_fresh = 0
    for low, high in ranges_no_overlap:
        total_fresh += (high - low + 1)

    print("Total Fresh IDs:", total_fresh)