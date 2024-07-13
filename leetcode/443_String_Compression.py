# https://leetcode.com/problems/string-compression/description/?envType=study-plan-v2&envId=leetcode-75
from typing import List

class Solution:
    def compress(self, chars: List[str]) -> int:
        chars_len = len(chars)
        start_idx = 0
        start_char = chars[0]
        result_idx = 0

        for i in range(chars_len + 1):
            if i == chars_len or start_char != chars[i]:
                start_char_len = i - start_idx
                chars[result_idx] = start_char
                if start_char_len > 1:
                    number = list(str(start_char_len))
                    for j, v in enumerate(number):
                        chars[result_idx + 1 + j] = v
                    result_idx += len(number) + 1
                else:
                    result_idx += 1

                if i < chars_len:
                    start_char = chars[i]
                start_idx = i

        print(chars)
        return result_idx


print(Solution().compress(["a","a","b","b","c","c","c"]))
print(Solution().compress(["a"]))
print(Solution().compress(["a","b","b","b","b","b","b","b","b","b","b","b","b"]))
print(Solution().compress(["a","a","a","b","b","a","a"]))
print(Solution().compress(["a","b","c"]))
