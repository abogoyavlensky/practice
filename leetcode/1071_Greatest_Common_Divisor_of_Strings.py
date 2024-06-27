# Link: https://leetcode.com/problems/greatest-common-divisor-of-strings/description/


def gcd(a_len, b_len):
    if b_len == 0:
        return a_len
    return gcd(b_len, a_len % b_len)
    
    

class Solution:
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        has_gcd = str1 + str2 == str2 + str1
        if not has_gcd:
            return ""

        gcd_value = gcd(len(str1), len(str2))

        return str1[0:gcd_value]
    

# print(Solution().gcdOfStrings("ABABAB", "ABAB"))
# print(Solution().gcdOfStrings("LEET", "CODE"))
# print(Solution().gcdOfStrings("ABCABC", "ABC"))
print(Solution().gcdOfStrings("ABABAB", "ABAB"))
print(Solution().gcdOfStrings("ABABABAB", "ABAB"))
