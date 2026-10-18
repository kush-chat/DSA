"""LeetCode 33: Search in Rotated Sorted Array (Medium).

https://leetcode.com/problems/search-in-rotated-sorted-array/
Return the target's index in a possibly rotated increasing array, or -1.
Constraints: 1 <= len(nums) <= 5000; -10_000 <= nums[i], target <= 10_000.
Values are unique. Neither approach modifies nums.
The linear baseline is educational; only the optimal approach satisfies the
problem's required O(log n) runtime.
"""


def search_lengthy(nums: list[int], target: int) -> int:
    """Scan every value regardless of rotation. Time: O(n). Space: O(1)."""
    for index, value in enumerate(nums):
        if value == target:
            return index
    return -1


def search_optimal(nums: list[int], target: int) -> int:
    """Identify the sorted half at each step. Time: O(log n). Space: O(1)."""
    left, right = 0, len(nums) - 1
    while left <= right:
        middle = left + (right - left) // 2
        if nums[middle] == target:
            return middle
        # With distinct values, at least one half is sorted normally.
        if nums[left] <= nums[middle]:
            if nums[left] <= target < nums[middle]:
                right = middle - 1
            else:
                left = middle + 1
        else:
            if nums[middle] < target <= nums[right]:
                left = middle + 1
            else:
                right = middle - 1
    return -1


class Solution:
    """LeetCode-compatible entry point."""

    def search(self, nums: list[int], target: int) -> int:
        return search_optimal(nums, target)


def main() -> None:
    cases = [([4, 5, 6, 7, 0, 1, 2], 0, 4), ([4, 5, 6, 7, 0, 1, 2], 3, -1),
             ([1], 0, -1), ([1], 1, 0), ([3, 1], 1, 1), ([3, 1], 3, 0),
             ([1, 2, 3, 4], 4, 3), ([5, 1, 2, 3, 4], 5, 0),
             ([2, 3, 4, 5, 1], 1, 4), ([10_000, -10_000, 0], -10_000, 1)]
    for nums, target, expected in cases:
        lengthy = search_lengthy(nums, target)
        optimal = search_optimal(nums, target)
        assert lengthy == optimal == expected, (nums, target, lengthy, optimal)
        print(f"nums={nums}, target={target}: lengthy={lengthy}, optimal={optimal}")


if __name__ == "__main__":
    main()
