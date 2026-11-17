"""34. Find First and Last Position of Element in Sorted Array — Medium.
https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/
Constraints: 0 <= len(nums) <= 100000; values and target in [-10**9, 10**9];
nums is nondecreasing. Solution uses the required logarithmic algorithm.
"""
from itertools import combinations_with_replacement


def search_range_straightforward(nums: list[int], target: int) -> list[int]:
    """Teaching baseline: two linear scans, O(n) time and O(1) extra space."""
    first = -1
    index = 0
    while index < len(nums):
        value = nums[index]
        if value == target:
            first = index
            break
        if value > target:
            # Sorted order rules out every remaining position.
            return [-1, -1]
        index += 1
    if first == -1:
        return [-1, -1]

    last = first
    index = len(nums) - 1
    while index >= first:
        if nums[index] == target:
            last = index
            break
        index -= 1
    return [first, last]


def search_range_optimal(nums: list[int], target: int) -> list[int]:
    """Two boundary searches: O(log(n+1)) time, O(1) extra space."""
    def boundary(after_equal: bool) -> int:
        left, right = 0, len(nums)
        # Search a half-open interval; len(nums) is a valid insertion index.
        while left < right:
            middle = (left + right) // 2
            if nums[middle] < target or (after_equal and nums[middle] == target):
                left = middle + 1
            else:
                right = middle
        return left

    first = boundary(False)  # First value >= target.
    if first == len(nums) or nums[first] != target:
        return [-1, -1]
    return [first, boundary(True) - 1]  # First value > target, minus one.


class Solution:
    def searchRange(self, nums: list[int], target: int) -> list[int]:
        return search_range_optimal(nums, target)


def check(nums, target, expected):
    original = nums.copy()
    assert search_range_straightforward(nums, target) == expected
    assert search_range_optimal(nums, target) == expected
    assert Solution().searchRange(nums, target) == expected
    assert nums == original


def main() -> None:
    for nums, target, expected in [
        ([5, 7, 7, 8, 8, 10], 8, [3, 4]),
        ([5, 7, 7, 8, 8, 10], 6, [-1, -1]),
        ([], 0, [-1, -1]), ([1], 1, [0, 0]), ([1], 0, [-1, -1]),
        ([-10**9, -10**9, 10**9], -10**9, [0, 1]),
        ([-10**9, 10**9, 10**9], 10**9, [1, 2]),
        ([0] * 100000, 0, [0, 99999]),
        ([0] * 100000, 1, [-1, -1]),
        (list(range(100000)), 99999, [99999, 99999]),
    ]:
        check(nums, target, expected)
    count = 0
    for size in range(9):
        for values in combinations_with_replacement(range(-2, 3), size):
            nums = list(values)
            for target in range(-3, 4):
                positions = [i for i, value in enumerate(nums) if value == target]
                expected = [positions[0], positions[-1]] if positions else [-1, -1]
                check(nums, target, expected)
                count += 1
    print(f'34: examples, bounds, and {count} exhaustive cases passed')


if __name__ == '__main__':
    main()
