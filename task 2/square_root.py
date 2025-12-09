def integer_sqrt(x):
    if x < 2:
        return x

    left, right = 1, x // 2
    while left <= right:
        mid = (left + right) // 2
        if mid * mid == x:
            return mid
        elif mid * mid < x:
            left = mid + 1
        else:
            right = mid - 1

    return right 


# Examples
print(integer_sqrt(4))  
print(integer_sqrt(8)) 
