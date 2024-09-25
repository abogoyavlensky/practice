# https://leetcode.com/problems/guess-number-higher-or-lower/description/?envType=study-plan-v2&envId=leetcode-75
# Topics: Binary Search, Interactive

PICK = 6

def guess(x):
    if x == PICK:
        return 0
    elif x < PICK:
        return 1
    else:
        return -1

class Solution:
    def guessNumber(self, n: int) -> int:
        left = 0
        right = n
        response = None

        while response != 0:
            my_guess = (left + right) // 2
            response = guess(my_guess)
            if response == -1:
                right = my_guess - 1
            elif response == 1:
                left = my_guess + 1
            else:
                result = my_guess
                break

        return result
    

print(Solution().guessNumber(10))
