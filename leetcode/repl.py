# 
# Topcis:
from typing import List
from itertools import islice

class Solution:
    def func(self, num: int) -> float:
        pass

# print(Solution().func(1))

####################################

# print(tuple(islice([1, 2, 3, 4, 5], 3)))


for i in islice([1, 2, 3, 4, 5], 3):
    print(i)
