"""LeetCode 64: Minimum Path Sum (Medium).

https://leetcode.com/problems/minimum-path-sum/
Find the smallest sum along a top-left to bottom-right path, moving right/down.
Constraints: 1 <= rows, columns <= 200; 0 <= grid[r][c] <= 200.
Both solutions preserve the input grid.
"""


def min_path_sum_lengthy(grid: list[list[int]]) -> int:
    """Full DP table. Time O(m*n), extra space O(m*n)."""
    rows, cols = len(grid), len(grid[0])
    costs = [[0] * cols for _ in range(rows)]
    costs[0][0] = grid[0][0]
    for row in range(1, rows):
        costs[row][0] = costs[row - 1][0] + grid[row][0]
    for col in range(1, cols):
        costs[0][col] = costs[0][col - 1] + grid[0][col]
    for row in range(1, rows):
        for col in range(1, cols):
            costs[row][col] = grid[row][col] + min(
                costs[row - 1][col], costs[row][col - 1])
    return costs[-1][-1]


def min_path_sum_optimal(grid: list[list[int]]) -> int:
    """Rolling DP. Time O(m*n), extra space O(min(m,n)); input unchanged."""
    rows, cols = len(grid), len(grid[0])
    # Traverse the conceptual transpose when it makes the saved frontier shorter.
    transposed = cols > rows
    outer, inner = (cols, rows) if transposed else (rows, cols)
    costs = [0] * inner
    for i in range(outer):
        for j in range(inner):
            value = grid[j][i] if transposed else grid[i][j]
            if i == 0 and j == 0:
                costs[j] = value
            elif i == 0:
                costs[j] = costs[j - 1] + value
            elif j == 0:
                costs[j] += value
            else:
                # costs[j] is from the previous frontier, costs[j-1] is current.
                costs[j] = min(costs[j], costs[j - 1]) + value
    return costs[-1]


class Solution:
    def minPathSum(self, grid: list[list[int]]) -> int:
        return min_path_sum_optimal(grid)


def main() -> None:
    cases = [([[1, 3, 1], [1, 5, 1], [4, 2, 1]], 7),
             ([[1, 2, 3], [4, 5, 6]], 12), ([[0]], 0), ([[200]], 200),
             ([[1, 2, 3]], 6), ([[1], [2], [3]], 6),
             ([[0, 0], [0, 0]], 0), ([[1, 100], [1, 1], [100, 1]], 4)]
    for grid, expected in cases:
        before = [row[:] for row in grid]
        lengthy = min_path_sum_lengthy(grid)
        optimal = min_path_sum_optimal(grid)
        assert lengthy == optimal == expected
        assert Solution().minPathSum(grid) == expected
        assert grid == before
        print(f'expected={expected}: lengthy={lengthy}, optimal={optimal}')


if __name__ == '__main__':
    main()
