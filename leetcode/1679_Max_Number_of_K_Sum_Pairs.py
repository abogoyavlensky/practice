# https://leetcode.com/problems/max-number-of-k-sum-pairs/description/?envType=study-plan-v2&envId=leetcode-75
# Topcis: Array, Hash Table, Two Pointers, Sorting

from typing import List

class Solution:
    def maxOperations(self, nums: List[int], k: int) -> int:
        op_counter = 0
        deleted_idx = set()

        for i, v in enumerate(nums):
            if i in deleted_idx:
                continue

            for j in range(i + 1, len(nums)):
                if j in deleted_idx:
                    continue

                if v + nums[j] == k:
                    op_counter += 1
                    deleted_idx.add(j)
                    break

        return op_counter


print(Solution().maxOperations(nums = [1,2,3,4], k = 5))
print(Solution().maxOperations(nums = [3,1,3,4,3], k = 6))
