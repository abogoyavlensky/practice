# https://leetcode.com/problems/maximum-average-subarray-i/?envType=study-plan-v2&envId=leetcode-75
# Topcis:Array, Sliding Window
from typing import List

class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        sub_array = nums[0:k]
        sub_sum = sum(sub_array)
        max_avg = sub_sum / k
        
        for i in range(k, len(nums)):
            sub_sum = sub_sum + nums[i] - nums[i - k]

            avg = sub_sum / k
            if max_avg < avg:
                max_avg = avg
        
        return max_avg


print(Solution().findMaxAverage(nums = [1,12,-5,-6,50,3], k = 4))
print(Solution().findMaxAverage(nums = [5], k = 1))
print(Solution().findMaxAverage(nums = [-1], k = 1))
print(Solution().findMaxAverage(nums = [1,12,-5,-6,50,3,1], k = 3))
print(Solution().findMaxAverage(nums = [1,12], k = 2))
