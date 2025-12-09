def two_sum(nums, target):
    seen = {}

    for i, num in enumerate(nums):
        needed = target - num

        if needed in seen:
            return [seen[needed], i]

        seen[num] = i


# Examples
print(two_sum([2, 7, 11, 15], 9))  
print(two_sum([3, 2, 4], 6))     
