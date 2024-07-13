# https://leetcode.com/problems/is-subsequence/description/?envType=study-plan-v2&envId=leetcode-75
# Topics: Two Pointers, String, Dynamic Programming

class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        s_idx = 0 

        for val in t:
            if len(s) == s_idx:
                return True

            if s and s[s_idx] == val:
                s_idx += 1

        return len(s) == s_idx


print(Solution().isSubsequence(s = "abc", t = "ahbgdc"))
print(Solution().isSubsequence(s = "axc", t = "ahbgdc"))
print(Solution().isSubsequence(s = "", t = "ahbgdc"))
print(Solution().isSubsequence(s = "b", t = "abc"))
