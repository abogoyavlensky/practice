# https://leetcode.com/problems/can-place-flowers/?envType=study-plan-v2&envId=leetcode-75

from typing import List

class Solution:
    def canPlaceFlowers(self, flowerbed: List[int], n: int) -> bool:
        last_idx = len(flowerbed) - 1
        prev_is_empty = True

        for i, v in enumerate(flowerbed):
            if n == 0:
                break

            if v == 0:
                if prev_is_empty and (i == last_idx or flowerbed[i + 1] == 0):
                    prev_is_empty = False
                    n -= 1
                else:
                    prev_is_empty = True
            else:
                prev_is_empty = False

        return n == 0

print(Solution().canPlaceFlowers([0,0,1,0,0], 1))
