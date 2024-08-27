# https://leetcode.com/problems/equal-row-and-column-pairs/description/?envType=study-plan-v2&envId=leetcode-75
# Topics: Array, Hash Table, Matrix, Simulation

class Solution:
    def equalPairs(self, grid: list[list[int]]) -> int:
        cols = []
        max_pair = 0

        for i in range(len(grid)):
            cur_col = []
            for j in range(len(grid)):
                cur_col.append(grid[j][i])

            cols.append(hash(tuple(cur_col)))

        for row in grid:
            cur_row = hash(tuple(row))
            for i in cols:
                if cur_row == i:
                    max_pair += 1

        return max_pair


print(Solution().equalPairs(grid = [[3,2,1],[1,7,6],[2,7,7]]))
print(Solution().equalPairs(grid = [[3,1,2,2],[1,4,4,5],[2,4,2,2],[2,4,2,2]]))
