numbers = list(map(int, input("Enter numbers separated by spaces: ").split()))

max_num = numbers[0]
for n in numbers:
    if n > max_num:
        max_num = n

print("Maximum number is:", max_num)
