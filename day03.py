def calculate_joltage(bank: str, n: int) -> int:
    """Calculate the joltage of a bank by selecting n largest digits in order."""
    position = -1
    digits = []
    while n > 0:
        next_largest_digit = max(int(digit) for digit in bank[position+1:len(bank)-n+1])
        position = bank.find(str(next_largest_digit), position+1)
        digits.append(next_largest_digit)
        n -= 1
    joltage = 0
    for i in range(len(digits)):
        joltage += digits[i] * (10 ** (len(digits) - i - 1))
    return joltage

if __name__ == "__main__":
    banks = []
    with open("inputs/day3.txt") as file:
        for line in file:
            banks.append(line.strip())

    # Part 1: Calculate joltage using 2 largest batteries in each bank
    joltages_part1 = [calculate_joltage(bank, 2) for bank in banks]
    print("Total Output Joltage:", sum(joltages_part1))

    # Part 2: Calculate joltage using 12 largest batteries in each bank
    joltages_part2 = [calculate_joltage(bank, 12) for bank in banks]
    print("New Total Output Joltage:", sum(joltages_part2))