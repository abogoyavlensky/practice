# https://leetcode.com/problems/find-the-highest-altitude/description/?envType=study-plan-v2&envId=leetcode-75
# Topcis: Array, Prefix Sum

class Solution:
    def largestAltitude(self, gain: list[int]) -> int:
        alt = 0 
        highest = 0 

        for i in gain:
            alt += i

            if alt > highest:
                highest = alt
        
        return highest
            


print(Solution().largestAltitude(gain = [-5,1,5,0,-7]))
print(Solution().largestAltitude(gain = [-4,-3,-2,-1,4,3,2]))
print(Solution().largestAltitude(gain = [44,32,-9,52,23,-50,50,33,-84,47,-14,84,36,-62,37,81,-36,-85,-39,67,-63,64,-47,95,91,-40,65,67,92,-28,97,100,81]))
