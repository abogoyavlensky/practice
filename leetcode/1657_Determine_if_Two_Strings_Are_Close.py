# https://leetcode.com/problems/determine-if-two-strings-are-close/?envType=study-plan-v2&envId=leetcode-75
# Topics: Hash Table, String, Sorting, Counting

class Solution:
    def closeStrings(self, word1: str, word2: str) -> bool:
        freq1 = {}
        for i in word1:
            if i in freq1:
                freq1[i] += 1
            else:
                freq1[i] = 1

        freq2 = {}
        for i in word2:
            if i in freq2:
                freq2[i] += 1
            else:
                freq2[i] = 1

        if not set(freq1.keys()) == set(freq2.keys()):
            return False
        
        if sorted(list(freq1.values())) == sorted(list(freq2.values())):
            return True
        
        return False
                


print(Solution().closeStrings(word1 = "abc", word2 = "bca"))
print(Solution().closeStrings(word1 = "a", word2 = "aa"))
print(Solution().closeStrings(word1 = "cabbba", word2 = "abbccc"))
