"""LeetCode 153: Find Minimum in Rotated Sorted Array (Medium).

https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/
Constraints: 1 <= len(nums) <= 5000; -5000 <= nums[i] <= 5000;
values are unique and the array is a rotation of a strictly increasing array.
Both solutions preserve the input. Only binary search meets the O(log n) goal.
"""


def find_min_lengthy(nums: list[int]) -> int:
    """Inspect every value. Time O(n), extra space O(1)."""
    smallest = nums[0]
    for index in range(1, len(nums)):
        if nums[index] < smallest:
            smallest = nums[index]
    return smallest


def find_min_optimal(nums: list[int]) -> int:
    """Keep the interval containing the minimum. Time O(log n), space O(1)."""
    left, right = 0, len(nums) - 1
    while left < right:
        middle = left + (right - left) // 2
        if nums[middle] > nums[right]:
            left = middle + 1  # The rotation boundary lies after middle.
        else:
            right = middle  # Middle may itself hold the minimum.
    return nums[left]


class Solution:
    def findMin(self, nums: list[int]) -> int:
        return find_min_optimal(nums)


def main() -> None:
    cases = [([3, 4, 5, 1, 2], 1), ([4, 5, 6, 7, 0, 1, 2], 0),
             ([11, 13, 15, 17], 11), ([7], 7), ([2, 1], 1),
             ([1, 2], 1), ([0, 5000, -5000], -5000), ([2, 3, 4, 1], 1)]
    for nums, expected in cases:
        before = nums[:]
        lengthy = find_min_lengthy(nums)
        optimal = find_min_optimal(nums)
        assert lengthy == optimal == expected
        assert Solution().findMin(nums) == expected
        assert nums == before
        print(f'{nums}: lengthy={lengthy}, optimal={optimal}')


if __name__ == '__main__':
    main()
