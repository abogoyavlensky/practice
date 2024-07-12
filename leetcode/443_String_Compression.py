# https://leetcode.com/problems/string-compression/description/?envType=study-plan-v2&envId=leetcode-75
from typing import List

class Solution:
    def compress(self, chars: List[str]) -> int:
        chars_len = len(chars)
        result = []
        start = 0 
        start_char = chars[0]
        start_char_len = 0

        for i in range(chars_len):
            if start_char == chars[i]:
                start_char_len += 1

            if start_char != chars[i] or i == chars_len - 1:
                result += [start_char]
                if start_char_len > 1:
                    result += list(str(start_char_len))
                start_char = chars[i]
                start_char_len = 1

        chars = result
        print(chars)
        return len(chars)


print(Solution().compress(["a","a","b","b","c","c","c"]))
print(Solution().compress(["a"]))
print(Solution().compress(["a","b","b","b","b","b","b","b","b","b","b","b","b"]))
