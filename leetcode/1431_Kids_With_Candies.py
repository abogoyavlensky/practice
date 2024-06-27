# Link: https://leetcode.com/problems/kids-with-the-greatest-number-of-candies/?envType=study-plan-v2&envId=leetcode-75
from typing import List

class Solution:
    def kidsWithCandies(self, candies: List[int], extraCandies: int) -> List[bool]:
        max_val = max(candies)
        result = []
        for v in candies:
            if (v + extraCandies) >= max_val:
                result.append(True)
            else:
                result.append(False)

        return result

print(Solution().kidsWithCandies([2,3,5,1,3], 3))
