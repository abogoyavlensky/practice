# https://leetcode.com/problems/dota2-senate/description/?envType=study-plan-v2&envId=leetcode-75
# Topics: String, Greedy, Queue
from collections import deque


class Solution:
    def predictPartyVictory(self, senate: str) -> str:
        stack = deque(list(senate))
        voted = deque([])
        not_voted = deque([])
        winner = None

        while not winner:
            for _ in range(len(stack)):
                i = stack.popleft()
                if not not_voted:
                    not_voted.append(i)
                    not_voted.append(i)
                else:
                    left = not_voted[0]
                    if left != i:
                        not_voted.popleft()
                        voted.append(left)
                    else:
                        not_voted.append(i)

            for _ in range(len(not_voted)):
                i = not_voted.popleft()
                for i in 

            if voted:
                stack.extend(voted)
            
            if not_voted:
                stack.extend(not_voted)
            
            voted = deque([])
            not_voted = deque([])

            if not stack:
                raise Exception("Stack is empty!")

            if len(set(stack)) == 1:
                winner = stack.pop()
                
        
        return 'Radiant' if winner == 'R' else 'Dire'



# print(Solution().predictPartyVictory(senate = "RD"))
# print(Solution().predictPartyVictory(senate = "RDD"))
# print(Solution().predictPartyVictory(senate = "RRRDDD"))
# print(Solution().predictPartyVictory(senate = "DDRRRD"))
# print(Solution().predictPartyVictory(senate = "DDRRR"))
print(Solution().predictPartyVictory(senate = "DRRDRDRDRDDRDRDR"))
