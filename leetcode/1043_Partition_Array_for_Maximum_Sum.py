# https://leetcode.com/problems/partition-array-for-maximum-sum/?envType=problem-list-v2&envId=array&difficulty=MEDIUM%2CEASY&status=TO_DO%2CATTEMPTED
# Topics: Array, Dynamic Programming

class Solution:
    def maxSumAfterPartitioning(self, arr: list[int], k: int) -> int:
        arr_len = len(arr)
        dp = [0] * (arr_len + 1)

        if arr_len == 1:
            return arr[0]

        for i in range(1, arr_len + 1):
            for j in range(1, min(i, k) + 1):
                prev_idx = i - j
                max_val = max(arr[prev_idx:i])
                sum_val = dp[prev_idx] + (max_val * j)
                if sum_val > dp[i]:
                    dp[i] = sum_val

        return dp[-1]




print(Solution().maxSumAfterPartitioning(arr = [1,15,7,9,2,5,10], k = 3))
print(Solution().maxSumAfterPartitioning(arr = [1,4,1,5,7,3,6,1,9,9,3], k = 4))
print(Solution().maxSumAfterPartitioning(arr = [1], k = 1))
