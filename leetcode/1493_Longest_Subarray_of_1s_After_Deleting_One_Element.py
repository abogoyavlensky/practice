# https://leetcode.com/problems/longest-subarray-of-1s-after-deleting-one-element/description/?envType=study-plan-v2&envId=leetcode-75
# Topcis: Array, Dynamic Programming, Sliding Window

class Solution:
    def longestSubarray(self, nums: list[int]) -> int:
        zero_count = 0
        max_seq = 0
        cur_seq = -1
        left_idx = 0
        i = 0

        while i < len(nums):
            if nums[i] == 1:
                cur_seq += 1
                i += 1
            elif nums[i] == 0:
                zero_count += 1
                if zero_count > 1:
                    if nums[left_idx] == 0:
                        zero_count -= 1
                        i += 1
                    else:
                        cur_seq -= 1
                    left_idx += 1
                else:
                    i += 1
                    cur_seq += 1

            if cur_seq > max_seq:
                max_seq = cur_seq
        
        return max_seq
        

print(Solution().longestSubarray(nums = [1,1,0,1]))
print(Solution().longestSubarray(nums = [0,1,1,1,0,1,1,0,1]))
print(Solution().longestSubarray(nums = [1,1,1]))
print(Solution().longestSubarray(nums = [0,1,1,1,0,0,1,1,0]))
