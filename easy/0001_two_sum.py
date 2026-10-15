"""LeetCode 1: Two Sum (Easy).

https://leetcode.com/problems/two-sum/
Return indices of two different elements whose sum equals target.
The problem guarantees exactly one answer; neither approach mutates nums.
"""


def two_sum_lengthy(nums: list[int], target: int) -> list[int]:
    """Try every pair. Time: O(n²). Extra space: O(1)."""
    for first in range(len(nums)):
        for second in range(first + 1, len(nums)):
            if nums[first] + nums[second] == target:
                return [first, second]
    raise ValueError("No pair adds up to target")


def two_sum_optimal(nums: list[int], target: int) -> list[int]:
    """Remember previously seen values. Expected time: O(n). Space: O(n)."""
    seen: dict[int, int] = {}
    for index, value in enumerate(nums):
        complement = target - value
        # Look up before inserting so the same index cannot be used twice.
        if complement in seen:
            return [seen[complement], index]
        seen[value] = index
    raise ValueError("No pair adds up to target")


class Solution:
    """LeetCode-compatible entry point using the interview solution."""

    def twoSum(self, nums: list[int], target: int) -> list[int]:
        return two_sum_optimal(nums, target)


def main() -> None:
    cases = [([2, 7, 11, 15], 9), ([3, 2, 4], 6), ([3, 3], 6),
             ([-3, 4, 3, 90], 0), ([0, 4, 3, 0], 0)]
    for nums, target in cases:
        lengthy = two_sum_lengthy(nums, target)
        optimal = two_sum_optimal(nums, target)
        for first, second in (lengthy, optimal):
            assert first != second and nums[first] + nums[second] == target
        print(f"nums={nums}, target={target}: lengthy={lengthy}, optimal={optimal}")


if __name__ == "__main__":
    main()
