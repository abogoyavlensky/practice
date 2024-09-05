# https://leetcode.com/problems/dota2-senate/description/?envType=study-plan-v2&envId=leetcode-75
# Topics: String, Greedy, Queue
from collections import deque


class Solution:
    def predictPartyVictory(self, senate: str) -> str:
        radiant = deque()
        dire = deque()
        
        # Enqueue each senator based on their party
        for i, s in enumerate(senate):
            if s == 'R':
                radiant.append(i)
            else:
                dire.append(i)
        
        n = len(senate)
        
        # Process the voting rounds
        while radiant and dire:
            r = radiant.popleft()
            d = dire.popleft()
            
            # The senator with the smaller index bans the other
            if r < d:
                radiant.append(r + n)  # Re-queue the Radiant senator
            else:
                dire.append(d + n)     # Re-queue the Dire senator
        
        # Return the party that has senators remaining
        return "Radiant" if radiant else "Dire"



print(Solution().predictPartyVictory(senate = "RD"))
print(Solution().predictPartyVictory(senate = "RDD"))
print(Solution().predictPartyVictory(senate = "RRRDDD"))
print(Solution().predictPartyVictory(senate = "DDRRRD"))
print(Solution().predictPartyVictory(senate = "DDRRR"))
print(Solution().predictPartyVictory(senate = "DRRDRDRDRDDRDRDR"))
