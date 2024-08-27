# https://leetcode.com/problems/find-the-difference-of-two-arrays/description/?envType=study-plan-v2&envId=leetcode-75
# Topics: Array, Hash Table

class Solution:
    def findDifference(self, nums1: list[int], nums2: list[int]) -> list[list[int]]:
        nums1_set = set(nums1)
        nums2_set = set(nums2)

        only_in_nums1 = []

        for i in nums1_set:
            if i not in nums2_set:
                only_in_nums1.append(i)

        only_in_nums2 = []

        for i in nums2_set:
            if i not in nums1_set:
                only_in_nums2.append(i)

        return [only_in_nums1, only_in_nums2]

print(Solution().findDifference(nums1 = [1,2,3], nums2 = [2,4,6]))
print(Solution().findDifference(nums1 = [1,2,3,3], nums2 = [1,1,2,2]))