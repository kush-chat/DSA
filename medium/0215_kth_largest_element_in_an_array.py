"""LeetCode 215: Kth Largest Element in an Array (Medium).

https://leetcode.com/problems/kth-largest-element-in-an-array/
Duplicates count separately in the rank.
Constraints: 1 <= k <= len(nums) <= 100_000; -10_000 <= nums[i] <= 10_000.
Both approaches preserve the input.
"""
from random import randrange


def kth_largest_lengthy(nums: list[int], k: int) -> int:
    """Sort a copy. Time O(n log n), extra space O(n)."""
    ordered = sorted(nums)
    target = len(ordered) - k
    return ordered[target]


def kth_largest_optimal(nums: list[int], k: int) -> int:
    """Randomized quickselect: expected O(n) time, worst O(n**2).

    Extra space O(n) for an input-preserving copy; partitioning uses O(1).
    Three-way partitioning handles many duplicate values efficiently.
    """
    values = nums[:]
    target = len(values) - k
    left, right = 0, len(values) - 1
    while left <= right:
        pivot = values[randrange(left, right + 1)]
        lower, scan, upper = left, left, right
        while scan <= upper:
            if values[scan] < pivot:
                values[lower], values[scan] = values[scan], values[lower]
                lower += 1
                scan += 1
            elif values[scan] > pivot:
                values[scan], values[upper] = values[upper], values[scan]
                upper -= 1  # The swapped-in value still needs inspection.
            else:
                scan += 1
        # [lower, upper] contains all values equal to the pivot.
        if target < lower:
            right = lower - 1
        elif target > upper:
            left = upper + 1
        else:
            return pivot
    raise AssertionError('Unreachable for valid k')


class Solution:
    def findKthLargest(self, nums: list[int], k: int) -> int:
        return kth_largest_optimal(nums, k)


def main() -> None:
    cases = [([3, 2, 1, 5, 6, 4], 2, 5),
             ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4, 4), ([7], 1, 7),
             ([2, 2, 2], 2, 2), ([-10000, 0, 10000], 3, -10000),
             ([-3, -1, -2], 1, -1), ([1, 2, 3], 1, 3)]
    for nums, k, expected in cases:
        before = nums[:]
        lengthy = kth_largest_lengthy(nums, k)
        optimal = kth_largest_optimal(nums, k)
        assert lengthy == optimal == expected
        assert Solution().findKthLargest(nums, k) == expected
        assert nums == before
        print(f'k={k}: lengthy={lengthy}, optimal={optimal}')


if __name__ == '__main__':
    main()
