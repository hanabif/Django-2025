def factorial(n):
    if n < 0:
        return "Factorial does not exist for negative numbers"
    if n == 0:
        return 1
    
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


num = int(input("Enter a number to find factorial: "))
print("Factorial:", factorial(num))
