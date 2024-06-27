# https://leetcode.com/problems/merge-strings-alternately/

class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        word1_last_idx = len(word1) - 1
        word2_last_idx = len(word2) - 1
        last_idx_min = min(word1_last_idx, word2_last_idx)
        result = ""
        
        i = 0
        while i <= last_idx_min:
            result += word1[i] + word2[i]
            i += 1

        if word1_last_idx < i <= word2_last_idx:
            index = i - 1 - word2_last_idx
            result += word2[index:]
        elif word2_last_idx < i <= word1_last_idx:
            index = i - 1 - word1_last_idx
            result += word1[index:]

        return result


print(Solution().mergeAlternately("abc", "pqrmmm"))

