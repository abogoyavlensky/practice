# https://leetcode.com/problems/number-of-recent-calls/?envType=study-plan-v2&envId=leetcode-75
# Topics: Design, Queue, Data Stream

from collections import deque


class RecentCounter:

    def __init__(self):
        self.requests = deque([])
        self.time_range_left = 0
        self.time_range_right = 0
        
    def last_requests_count(self):
        return len(self.requests)

    def ping(self, t: int) -> int:
        self.requests.append(t)
        self.time_range_left = t - 3000
        self.time_range_right = t

        while self.requests:
            item = self.requests.popleft()
            if item >= self.time_range_left:
                self.requests.appendleft(item)
                break
        
        return self.last_requests_count()
        


# Your RecentCounter object will be instantiated and called as such:
# obj = RecentCounter()
# param_1 = obj.ping(t)

obj = RecentCounter()
print(obj.ping(1))
print(obj.ping(100))
print(obj.ping(3001))
print(obj.ping(3002))
