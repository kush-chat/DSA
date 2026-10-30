"""LeetCode 62: Unique Paths (Medium).

https://leetcode.com/problems/unique-paths/
Count paths moving only right or down across an m-by-n grid.
Constraints: 1 <= m, n <= 100; the answer is at most 2 * 10**9.
"""


def unique_paths_lengthy(m: int, n: int) -> int:
    """Full dynamic programming table. Time O(m*n), extra space O(m*n)."""
    paths = [[0] * n for _ in range(m)]
    for row in range(m):
        paths[row][0] = 1
    for col in range(n):
        paths[0][col] = 1
    for row in range(1, m):
        for col in range(1, n):
            paths[row][col] = paths[row - 1][col] + paths[row][col - 1]
    return paths[-1][-1]


def unique_paths_optimal(m: int, n: int) -> int:
    """Binomial coefficient. O(min(m,n)) arithmetic steps, O(1) variables.

    Complexity uses unit-cost integer arithmetic; Python integers grow with the
    answer. Exact integer division avoids floating-point rounding errors.
    """
    # Choose where the less frequent move occurs among all m+n-2 moves.
    moves = m + n - 2
    chosen = min(m - 1, n - 1)
    result = 1
    for i in range(1, chosen + 1):
        # After iteration i, result equals C(moves-chosen+i, i).
        result = result * (moves - chosen + i) // i
    return result


class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        return unique_paths_optimal(m, n)


def main() -> None:
    for m, n, expected in [(3, 7, 28), (3, 2, 3), (1, 1, 1),
                           (1, 100, 1), (100, 1, 1), (2, 2, 2),
                           (10, 10, 48620)]:
        lengthy = unique_paths_lengthy(m, n)
        optimal = unique_paths_optimal(m, n)
        assert lengthy == optimal == expected
        assert Solution().uniquePaths(m, n) == expected
        print(f'{m}x{n}: lengthy={lengthy}, optimal={optimal}')


if __name__ == '__main__':
    main()
