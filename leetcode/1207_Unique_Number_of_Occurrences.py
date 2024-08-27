# https://leetcode.com/problems/unique-number-of-occurrences/description/?envType=study-plan-v2&envId=leetcode-75
# Topics: Array, Hash Table

class Solution:
    def uniqueOccurrences(self, arr: list[int]) -> bool:
        freq = {}

        for i in arr:
            if i in freq:
                freq[i] += 1
            else:
                freq[i] = 1

        check = set()
        for v in freq.values():
            if v in check:
                return False
            else:
                check.add(v)

        return True


print(Solution().uniqueOccurrences(arr = [1,2,2,1,1,3]))
print(Solution().uniqueOccurrences(arr = [1,2]))
print(Solution().uniqueOccurrences(arr = [-3,0,1,-3,1,1,1,-3,10,0]))