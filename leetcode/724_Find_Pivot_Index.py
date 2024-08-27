# https://leetcode.com/problems/find-pivot-index/?envType=study-plan-v2&envId=leetcode-75
# Topcis: Array, Prefix Sum

class Solution:
    def pivotIndex(self, nums: list[int]) -> int:
        len_nums = len(nums)
        left_sum_arr = []
        right_sum_arr = []

        left_sum = 0

        for i in nums:
            left_sum_arr.append(left_sum)
            left_sum += i

        right_sum = 0

        for i in range(len_nums - 1, -1, -1):
            right_sum_arr.append(right_sum)
            right_sum += nums[i]

        right_sum_arr.reverse()

        for i in range(len_nums):
            if left_sum_arr[i] == right_sum_arr[i]:
                return i
        
        return -1



print(Solution().pivotIndex(nums = [1,7,3,6,5,6]))
print(Solution().pivotIndex(nums = [1,2,3]))
print(Solution().pivotIndex(nums = [2,1,-1]))
