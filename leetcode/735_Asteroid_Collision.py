# https://leetcode.com/problems/asteroid-collision/description/?envType=study-plan-v2&envId=leetcode-75
# Topics: Array, Stack, Simulation

class Solution:
    def asteroidCollision(self, asteroids: list[int]) -> list[int]:
        stack = []

        for i in asteroids:
            if len(stack) == 0:
                stack.append(i)
                continue

            for _ in range(len(stack)):
                if stack[-1] > 0 and i < 0:
                    if abs(i) > abs(stack[-1]):
                        stack.pop()
                        # if last item in stack
                        if len(stack) == 0:
                            stack.append(i)
                            break
                    elif abs(i) == abs(stack[-1]):
                        stack.pop()
                        break
                    else:
                        break
                else:
                    stack.append(i)
                    break
            
        return stack



print(Solution().asteroidCollision(asteroids = [5,10,-5]))
print(Solution().asteroidCollision(asteroids = [8,-8]))
print(Solution().asteroidCollision(asteroids = [10,2,-5]))
print(Solution().asteroidCollision(asteroids = [-2,-1,1,2]))
print(Solution().asteroidCollision(asteroids = [-2,-2,1,-2]))
print(Solution().asteroidCollision(asteroids = [1,1,-2,-2]))
print(Solution().asteroidCollision(asteroids = [1,-2,-2,-2]))
