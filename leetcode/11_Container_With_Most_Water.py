# https://leetcode.com/problems/container-with-most-water/?envType=study-plan-v2&envId=leetcode-75
# Topcis: Array, Two Pointers, Greedy

from typing import List

class Solution:
    def maxArea(self, height: List[int]) -> int:
        left = 0
        right = len(height) - 1
        max_area = 0

        while left != right:
            x = right - left
            y = min(height[right], height[left])
            current_area = x * y
            if current_area >  max_area:
                max_area = current_area
            
            if height[left] > height[right]:
                right -= 1
            else:
                left += 1
        
        return max_area



print(Solution().maxArea([1,8,6,2,5,4,8,3,7]))
print(Solution().maxArea([1,1]))
