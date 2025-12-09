def pali(x):
    x_str = str(x)
    return x_str == x_str[::-1]


# Examples
print(pali(121))  
print(pali(-121)) 

