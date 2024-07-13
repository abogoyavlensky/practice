# https://leetcode.com/problems/move-zeroes/description/?envType=study-plan-v2&envId=leetcode-75
# Topics: two pointers, array
from typing import List

class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        nums_len = len(nums)
        num_idx = 1

        for i in range(nums_len):
            if nums[i] == 0 and i != nums_len - 1:
                should_stop = False
                for j in range(num_idx, nums_len):
                    if nums[j] != 0:
                        nums[i] = nums[j]
                        nums[j] = 0
                        num_idx = j + 1
                        break
                    elif nums[j] == 0 and j == nums_len - 1:
                        should_stop = True
                        break
                if should_stop:
                    break
            else: 
                num_idx += 1

        print(nums)
        return None
        

print(Solution().moveZeroes([0,1,0,3,12]))
print(Solution().moveZeroes([0]))
print(Solution().moveZeroes([0, 1]))
print(Solution().moveZeroes([0, 0, 0, 3, 0, 1]))
print(Solution().moveZeroes([4,2,4,0,0,3,0,5,1,0]))
