class Solution:
    def reverseWords(self, s: str):
        words = s.split()
        words.reverse()
        return ' '.join(words)

print(Solution().reverseWords("the sky is blue"))