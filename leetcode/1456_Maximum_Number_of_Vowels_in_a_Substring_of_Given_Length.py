# https://leetcode.com/problems/maximum-number-of-vowels-in-a-substring-of-given-length/?envType=study-plan-v2&envId=leetcode-75
# Topcis: String, Sliding Window

class Solution:
    def maxVowels(self, s: str, k: int) -> int:
        vowels = ["a", "e", "i", "o", "u"]

        cur_vowel_count = 0
        for i in range(k):
            if s[i] in vowels:
                cur_vowel_count += 1

        max_vowel_count = cur_vowel_count

        for i in range(k, len(s)):
            if s[i] in vowels:
                cur_vowel_count += 1

            if s[i - k] in vowels:
                cur_vowel_count -= 1

            if max_vowel_count < cur_vowel_count:
                max_vowel_count = cur_vowel_count

        return max_vowel_count


print(Solution().maxVowels(s = "abciiidef", k = 3))
print(Solution().maxVowels(s = "aeiou", k = 2))
print(Solution().maxVowels(s = "leetcode", k = 3))
