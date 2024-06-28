# https://leetcode.com/problems/can-place-flowers/?envType=study-plan-v2&envId=leetcode-75
# Note: Slow! Try to improve.

class Solution:
    def reverseVowels(self, s: str) -> str:
        vowels = {"a", "e", "i", "o", "u"}
        a = 0
        b = len(s) - 1
        first_part = ""
        second_part = ""

        while a <= b:
            if s[a].lower() in vowels:
                if s[b].lower() in vowels:
                    first_part = first_part + s[b]
                    if a != b:
                        second_part = s[a] + second_part
                    a += 1
                    b -= 1
                else:
                    second_part = s[b] + second_part
                    b -= 1
            else:
                first_part = first_part + s[a]
                a += 1
        return first_part + second_part


# print(Solution().reverseVowels("hello"))
# print(Solution().reverseVowels("leetcode"))
# print(Solution().reverseVowels("a."))
# print(Solution().reverseVowels("a"))
print(Solution().reverseVowels("ab"))
print(Solution().reverseVowels("ao"))
print(Solution().reverseVowels("."))
