def apply_operations(numbers: list[list[int]], operations: list[str]) -> list[int]:
    results = []
    for i, operation in enumerate(operations):
        if operation == "+":  
            result = sum(numbers[i])
        elif operation == "*":
            result = 1
            for num in numbers[i]:
                result *= num
        results.append(result)
    return results

if __name__ == "__main__":
    lines = []
    lines_2 = []
    operations = []
    with open("inputs/day6.txt") as file:
        for line in file:
            if line.startswith("+") or line.startswith("*"):
                operations.append([str(oper) for oper in line.strip().split() if oper.startswith(("+", "*"))])
            else:
                lines.append([int(num) for num in line.split() if num.isdigit()])
                lines_2.append(line.rstrip("\n"))

    # Part 1: Calculate grand total by performing operations column-wise
    operations = operations[0]
    lines = [list(row) for row in zip(*lines)]
    
    results = apply_operations(lines, operations)

    print("Grand Total:", sum(results))

    # Part 2: Right-to-left columns for each digit position
    columns = []
    column = []
    for i in range(len(lines_2[0])-1, -1, -1):
        all_empty = True
        number = ""
        for line in lines_2:
            if line[i] != " ":
                all_empty = False
                number += line[i]
        if all_empty:
            columns.append(column)
            column = []
        else:
            column.append(int(number))
            all_empty = True
    columns.append(column)
    
    results = apply_operations(columns, reversed(operations))
    
    print("Grand Total with right-to-left columns:", sum(results))