"""LeetCode 704: Binary Search (Easy).

https://leetcode.com/problems/binary-search/
Return the target's index in a strictly increasing array, or -1 if absent.
Constraints: 1 <= len(nums) <= 10_000; -10_000 < nums[i], target < 10_000.
Values are unique. Neither approach modifies nums.
The linear baseline is educational; only the optimal approach satisfies the
problem's required O(log n) runtime.
"""


def search_lengthy(nums: list[int], target: int) -> int:
    """Check values one by one. Time: O(n). Extra space: O(1)."""
    for index, value in enumerate(nums):
        if value == target:
            return index
        if value > target:
            break
    return -1


def search_optimal(nums: list[int], target: int) -> int:
    """Halve an inclusive search interval. Time: O(log n). Space: O(1)."""
    left, right = 0, len(nums) - 1
    while left <= right:
        middle = left + (right - left) // 2
        if nums[middle] == target:
            return middle
        # Sorted order rules out the midpoint and one entire half.
        if nums[middle] < target:
            left = middle + 1
        else:
            right = middle - 1
    return -1


class Solution:
    """LeetCode-compatible entry point."""

    def search(self, nums: list[int], target: int) -> int:
        return search_optimal(nums, target)


def main() -> None:
    cases = [([-1, 0, 3, 5, 9, 12], 9, 4), ([-1, 0, 3, 5, 9, 12], 2, -1),
             ([5], 5, 0), ([5], -1, -1), ([1, 3], 3, 1),
             ([-9999, 0, 9999], -9999, 0), ([-9999, 0, 9999], 9999, 2),
             ([1, 3], 0, -1), ([1, 3], 4, -1)]
    for nums, target, expected in cases:
        lengthy = search_lengthy(nums, target)
        optimal = search_optimal(nums, target)
        assert lengthy == optimal == expected, (nums, target, lengthy, optimal)
        print(f"nums={nums}, target={target}: lengthy={lengthy}, optimal={optimal}")


if __name__ == "__main__":
    main()
