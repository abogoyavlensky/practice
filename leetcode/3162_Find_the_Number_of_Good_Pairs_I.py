# https://leetcode.com/problems/find-the-number-of-good-pairs-i/?envType=problem-list-v2&envId=array&difficulty=MEDIUM%2CEASY&status=TO_DO%2CATTEMPTED
# Topics: Array, Hash Table

class Solution:
    def numberOfPairs(self, nums1: list[int], nums2: list[int], k: int) -> int:
        pair_number = 0

        for i  in nums1:
            for j in nums2:
                (_, mod) = divmod(i, j * k)
                if not mod:
                    pair_number += 1
        return pair_number


print(Solution().numberOfPairs(nums1 = [1,3,4], nums2 = [1,3,4], k = 1))
print(Solution().numberOfPairs(nums1 = [1,2,4,12], nums2 = [2,4], k = 3))
