# https://leetcode.com/problems/removing-stars-from-a-string/?envType=study-plan-v2&envId=leetcode-75
# Topics: String, Stack, Simulation

class Solution:
    def removeStars(self, s: str) -> str:
        stack = []

        for i in s:
            if i == "*":
                stack.pop()
            else:
                stack.append(i)

        return "".join(stack)


print(Solution().removeStars(s = "leet**cod*e"))
print(Solution().removeStars(s = "erase*****"))
