# https://leetcode.com/problems/delete-the-middle-node-of-a-linked-list/?envType=study-plan-v2&envId=leetcode-75
# Topics: Linked List, Two Pointers

# Definition for singly-linked list.
import copy
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def deleteMiddle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        list_len = 1
        item = copy.deepcopy(head)
        while item.next:
            item = item.next
            list_len += 1

        middle_idx, _  = divmod(list_len, 2)


        list_idx = 0
        item = copy.deepcopy(head)
        next_item = item
        pre_middle_node = None
        while next_item.next:
            if list_idx == middle_idx - 1:
                pre_middle_node = item
                break

            next_item = next_item.next
            list_idx += 1
        
        pre_middle_node.next = pre_middle_node.next.next

        return item




def make_list(input_arr: list):
    updated = [ListNode(val = i) for i in input_arr]
    for i in range(len(input_arr) - 1):
        updated[i].next = updated[i + 1]
    
    return updated[0]
        
    
list1_head = make_list([1,3,4,7,1,2,6])
print(Solution().deleteMiddle(list1_head))
