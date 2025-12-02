def find_divisors(n):
    divisors = []
    for i in range(2, int(n/2) + 1):
        if n % i == 0:
            divisors.append(i)
    divisors.append(1)
    divisors = divisors[::-1]
    return divisors

if __name__ == "__main__":
    with open("inputs/day2.txt") as file:
        line = file.readline().strip()
        id_range_list = line.split(',')
    
    invalid_ids_part1 = []
    invalid_ids_part2 = []

    for id_range in id_range_list:
        
        start, end = map(int, id_range.split('-'))
        
        for id in range(start, end + 1):
        
            num_digits = len(str(id))
        
            if num_digits == 1:
                continue
        
            divisor_list = find_divisors(num_digits)
        
            for divisor in divisor_list:
        
                sequence = id % 10**divisor
                number_to_check = 0
                n = num_digits - divisor
        
                while n >= 0:
                    number_to_check += sequence * 10**n
                    n -= divisor
        
                if number_to_check == id:
                    # Part 2: Find numbers that are made of repeated sequences
                    invalid_ids_part2.append(id)

                    # Part 1: Find numbers that are made of two identical halves
                    if num_digits % 2 == 0:     
                        if num_digits / divisor == 2 or divisor == 1:
                            invalid_ids_part1.append(id)
                    break
    
    print(f"Sum of invalid IDs (Part 1): {sum(invalid_ids_part1)}")
    print(f"Sum of invalid IDs (Part 2): {sum(invalid_ids_part2)}")

