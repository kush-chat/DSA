"""LeetCode 70: Climbing Stairs (Easy).

https://leetcode.com/problems/climbing-stairs/
Count ordered ways to climb n stairs using steps of size one or two.
Constraint: 1 <= n <= 45.
Both approaches use dynamic programming; the interview version stores only
the two previous results rather than a full table.
"""


def climb_stairs_lengthy(n: int) -> int:
    """Build a table for every stair. Time: O(n). Extra space: O(n)."""
    ways = [0] * (n + 1)
    ways[0] = 1  # One empty sequence is the base for taking the first step.
    ways[1] = 1
    for stair in range(2, n + 1):
        one_step_finish = ways[stair - 1]
        two_step_finish = ways[stair - 2]
        ways[stair] = one_step_finish + two_step_finish
    return ways[n]


def climb_stairs_optimal(n: int) -> int:
    """Roll the two needed DP states. Time: O(n). Extra space: O(1)."""
    two_back, one_back = 1, 1
    for stair in range(2, n + 1):
        two_back, one_back = one_back, two_back + one_back
    return one_back


class Solution:
    """LeetCode-compatible entry point."""

    def climbStairs(self, n: int) -> int:
        return climb_stairs_optimal(n)


def main() -> None:
    cases = [(1, 1), (2, 2), (3, 3), (4, 5), (5, 8),
             (10, 89), (45, 1_836_311_903)]
    for n, expected in cases:
        lengthy = climb_stairs_lengthy(n)
        optimal = climb_stairs_optimal(n)
        assert lengthy == optimal == expected, (n, lengthy, optimal)
        print(f"n={n}: lengthy={lengthy}, optimal={optimal}")


if __name__ == "__main__":
    main()
