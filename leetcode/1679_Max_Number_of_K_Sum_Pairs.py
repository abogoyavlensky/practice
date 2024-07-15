# https://leetcode.com/problems/max-number-of-k-sum-pairs/description/?envType=study-plan-v2&envId=leetcode-75
# Topcis: Array, Hash Table, Two Pointers, Sorting

from typing import List

class Solution:
    def maxOperations(self, nums: List[int], k: int) -> int:
        op_counter = 0
        # deleted_idx = set()

        # for i, v in enumerate(nums):
        #     if i in deleted_idx:
        #         continue

        #     for j in range(i + 1, len(nums)):
        #         if j in deleted_idx:
        #             continue

        #         if v + nums[j] == k:
        #             op_counter += 1
        #             deleted_idx.add(j)
        #             break

        numbers_freq = {}

        for i in nums:
            if i not in numbers_freq:
                numbers_freq[i] = 1
            else:
                numbers_freq[i] += 1

        for i in set(numbers_freq.keys()):
            required_num = k - i
            if i in numbers_freq and i == required_num:
                operations = numbers_freq[i] // 2
                op_counter += operations
                numbers_freq[i] -= operations * 2
            elif i in numbers_freq and required_num in numbers_freq:
                pairs_count = min(numbers_freq[i], numbers_freq[required_num])
                op_counter += pairs_count
                
                numbers_freq[i] -= pairs_count
                if numbers_freq[i] == 0:
                    del numbers_freq[i]

                numbers_freq[required_num] -= pairs_count
                if numbers_freq[required_num] == 0:
                    del numbers_freq[required_num]
            

        print(numbers_freq)
        return op_counter


print(Solution().maxOperations(nums = [1,2,3,4], k = 5))
print(Solution().maxOperations(nums = [3,1,3,4,3], k = 6))
