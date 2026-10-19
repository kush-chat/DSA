"""LeetCode 198: House Robber (Medium).

https://leetcode.com/problems/house-robber/
Find the largest sum of house values without selecting adjacent houses.
Constraints: 1 <= len(nums) <= 100; 0 <= nums[i] <= 400.
Neither approach mutates nums. The table approach exposes every subproblem;
the optimal interview approach keeps only the two needed states.
"""


def rob_lengthy(nums: list[int]) -> int:
    """Store the best result for each prefix. Time: O(n). Space: O(n)."""
    best = [0] * (len(nums) + 1)
    best[1] = nums[0]
    for count in range(2, len(nums) + 1):
        skip_current = best[count - 1]
        take_current = best[count - 2] + nums[count - 1]
        best[count] = max(skip_current, take_current)
    return best[-1]


def rob_optimal(nums: list[int]) -> int:
    """Roll the prefix DP states. Time: O(n). Extra space: O(1)."""
    two_back = one_back = 0
    for amount in nums:
        # Taking this house excludes its neighbor; skipping preserves one_back.
        current = max(one_back, two_back + amount)
        two_back, one_back = one_back, current
    return one_back


class Solution:
    """LeetCode-compatible entry point."""

    def rob(self, nums: list[int]) -> int:
        return rob_optimal(nums)


def main() -> None:
    cases = [([1, 2, 3, 1], 4), ([2, 7, 9, 3, 1], 12),
             ([0], 0), ([400], 400), ([2, 1], 2), ([1, 2], 2),
             ([2, 1, 1, 2], 4), ([0, 0, 0], 0), ([5, 5, 5], 10),
             ([400] * 100, 20_000)]
    for nums, expected in cases:
        lengthy = rob_lengthy(nums)
        optimal = rob_optimal(nums)
        assert lengthy == optimal == expected, (nums, lengthy, optimal)
        print(f"nums={nums}: lengthy={lengthy}, optimal={optimal}")


if __name__ == "__main__":
    main()
