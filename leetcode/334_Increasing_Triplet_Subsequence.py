# https://leetcode.com/problems/increasing-triplet-subsequence/description/?envType=study-plan-v2&envId=leetcode-75
# Topics: Dynamic Programming
from typing import List

# Solution1. Using dynamic prograrmming, slow.
class SolutionDP:
    def increasingTriplet(self, nums: List[int]) -> bool:
        n = len(nums)

        if n < 3:
            return False

        dp = [1] * n

        for i in range(1, n):
            for j in range(i):
                if nums[i] > nums[j]:
                    dp[i] = max(dp[i], dp[j] + 1)

        return max(dp) >= 3


print(SolutionDP().increasingTriplet([2,1,5,0,4,6]))
print(SolutionDP().increasingTriplet([5,4,3,2,1]))
print(SolutionDP().increasingTriplet([1,2,3,4,5]))
print(SolutionDP().increasingTriplet([20,100,10,12,5,13]))

# Solution2. O(n), fast.
class SolutionOn:
    def increasingTriplet(self, nums: List[int]) -> bool:
        n = len(nums)

        if n < 3:
            return False

        first = float('inf')
        second = float('inf')

        for i in nums:
            if i <= first:
                first = i
            elif i <= second:
                second = i
            else:
                return True

        return False


print(SolutionOn().increasingTriplet([2,1,5,0,4,6]))
print(SolutionOn().increasingTriplet([5,4,3,2,1]))
print(SolutionOn().increasingTriplet([1,2,3,4,5]))
print(SolutionOn().increasingTriplet([20,100,10,12,5,13]))
