# https://leetcode.com/problems/reverse-words-in-a-string/?envType=study-plan-v2&envId=leetcode-75

class Solution:
    def reverseWords(self, s: str):
        words = s.split()
        words.reverse()
        return ' '.join(words)

print(Solution().reverseWords("the sky is blue"))
