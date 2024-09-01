# https://leetcode.com/problems/decode-string/description/?envType=study-plan-v2&envId=leetcode-75
# Topics: String, Stack, Recursion

def parse(s, result_str):
    num_str = ''
    repeat_str = ''
    start_repeat = False
    brackets = []
    for i in s:
        if i == ']':
            brackets.pop()
            if not brackets:
                start_repeat = False
                result_str += parse(repeat_str, '') * int(num_str)
                repeat_str = ''
                num_str = ''
            else:
                repeat_str += i
        else:
            if start_repeat:
                repeat_str += i
                if i == '[':
                    brackets += i
            else:
                if i.isdigit():
                    num_str += i
                elif i == '[':
                    brackets += i
                    start_repeat = True
                else:
                    result_str += i
    
    return result_str


class Solution:
    def decodeString(self, s: str) -> str:
        return parse(s, '')

        

print(Solution().decodeString(s = "3[a]2[bc]ef"))
print(Solution().decodeString(s = "3[a2[c]]"))
print(Solution().decodeString(s = "2[abc]3[cd]ef"))
