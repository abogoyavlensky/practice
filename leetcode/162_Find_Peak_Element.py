# https://leetcode.com/problems/find-peak-element/description/?envType=study-plan-v2&envId=leetcode-75
# Topics: Array, Binary Search

def get_direction(nums, middle_idx):
    left_val = nums[middle_idx - 1] if middle_idx > 0 else None
    right_val = nums[middle_idx + 1] if middle_idx < len(nums) - 1 else None
    if (left_val is None or left_val <= nums[middle_idx]) \
        and (right_val is not None and nums[middle_idx] <= right_val):
        return "right"
    elif (left_val is None or left_val <= nums[middle_idx]) \
        and (right_val is None or right_val <= nums[middle_idx]):
        return "pick"
    
    else:
        return "left"


class Solution:
    def findPeakElement(self, nums: list[int]) -> int:
        result = None

        left_idx = 0
        right_idx = len(nums) - 1
        if left_idx == right_idx:
            return 0

        while (left_idx <= right_idx) or result is None:
            middle_idx = (left_idx + right_idx) // 2
            direction = get_direction(nums, middle_idx)

            if direction == "left": 
                right_idx = middle_idx - 1
            elif direction == "right" == direction:
                left_idx = middle_idx + 1
            else:
                result = middle_idx
                break

        return result

        

# print(Solution().findPeakElement(nums = [1]))
print(Solution().findPeakElement(nums = [1, 2]))
# print(Solution().findPeakElement(nums = [1,2,3,1]))
# print(Solution().findPeakElement(nums = [1,2,1,3,5,6,4]))
