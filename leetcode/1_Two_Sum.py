# https://leetcode.com/problems/two-sum/description/?envType=problem-list-v2&envId=array&difficulty=MEDIUM%2CEASY&status=TO_DO%2CATTEMPTED
# Topics: Array, Hash Table

# Works, but slow.
# class Solution:
#     def twoSum(self, nums: list[int], target: int) -> list[int]:
#         nums_len = len(nums)
#         nums_idxes = [[i, v] for i, v in enumerate(nums)]
#         nums_sorted = sorted(nums_idxes, key=lambda x: x[1])

#         for i in range(nums_len):
#             for j in range(i + 1, nums_len):
#                 result = nums_sorted[i][1] + nums_sorted[j][1]
#                 if result == target:
#                     return [nums_sorted[i][0], nums_sorted[j][0]] 
#                 elif result > target:
#                     break

#         return

# Fast solution
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        nums_freq = {}

        for i, v in enumerate(nums):
            if v not in nums_freq:
                nums_freq[v] = [i]
            else:
                nums_freq[v] + [i]
        
        for i, v in enumerate(nums):
            second_num = target - v
            existing = nums_freq.get(second_num)
            if existing and (len(existing) >= 1) and i not in existing:
                return [i, existing[0]]
            elif existing and len(existing) > 1 and i in existing:
                existing.remove(i)
                return [i, existing[0]]
            


print(Solution().twoSum(nums = [2,7,11,15], target = 9))
print(Solution().twoSum(nums = [3,2,4], target = 6))
print(Solution().twoSum(nums = [3,3], target = 6))
print(Solution().twoSum(nums = [0,4,3,0], target = 0))
