# https://leetcode.com/problems/successful-pairs-of-spells-and-potions/description/?envType=study-plan-v2&envId=leetcode-75
# Topics: Array, Two Pointers, Binary Search, Sorting

class Solution:
    def successfulPairs(self, spells: list[int], potions: list[int], success: int) -> list[int]:
        potions_sorted = sorted(potions)
        result = []

        for i in spells:
            num, m = divmod(success, i)
            target = num + 1 if m > 0 else num

            last_num = target + 1
            last_num_idx = -1
            left_idx = 0
            right_idx = len(potions_sorted) - 1
            while (left_idx <= right_idx) and (last_num >= target):
                middle_idx = (left_idx + right_idx) // 2
                if potions_sorted[middle_idx] >= target:
                    last_num = potions_sorted[middle_idx]
                    last_num_idx = middle_idx
                    right_idx = middle_idx - 1
                else:
                    left_idx = middle_idx + 1
            
            if last_num_idx > -1:
                pair_count = len(potions_sorted) - last_num_idx
            else: 
                pair_count = 0
            result.append(pair_count)

        return result


print(Solution().successfulPairs(spells = [5,1,3], potions = [1,2,3,4,5], success = 7))
print(Solution().successfulPairs(spells = [3,1,2], potions = [8,5,8], success = 16))
