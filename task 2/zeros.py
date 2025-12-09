def move(nums):
    insert_pos = 0

    for i in range(len(nums)):
        if nums[i] != 0:
            nums[insert_pos] = nums[i]
            insert_pos += 1

    for i in range(insert_pos, len(nums)):
        nums[i] = 0



nums1 = [0, 1, 0, 3, 12]
move(nums1)
print(nums1)  

nums2 = [0]
move(nums2)
print(nums2)
