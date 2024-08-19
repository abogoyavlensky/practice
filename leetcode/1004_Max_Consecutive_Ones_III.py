# https://leetcode.com/problems/max-consecutive-ones-iii/description/?envType=study-plan-v2&envId=leetcode-75
# Topcis: Array, Binary Search, Sliding Window, Prefix Sum
from typing import List

class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:
        max_num = 0
        current_num = 0
        left_idx = 0
        zero_count = 0

        for i in range(len(nums)):
            if nums[i] == 0:
                zero_count += 1
            
            if zero_count > k:
                if nums[left_idx] == 0:
                    zero_count -= 1

                left_idx += 1
            else:
                current_num += 1

            if max_num < current_num:
                max_num = current_num

        return max_num
        

print(Solution().longestOnes(nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2))
print(Solution().longestOnes(nums = [0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], k = 3))
print(Solution().longestOnes(nums = [1], k = 0))
print(Solution().longestOnes(nums = [0], k = 0))
