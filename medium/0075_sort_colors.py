"""75. Sort Colors — Medium.
https://leetcode.com/problems/sort-colors/

Constraints: 1 <= len(nums) <= 300; each element is 0, 1, or 2.
Both solutions mutate the original list and return None, without library sorting.
"""


def sort_colors_straightforward(nums: list[int]) -> None:
    """Count then overwrite: O(n) time, O(1) extra space; two passes.
    Explicit counts make the reconstruction easy to follow.
    """
    zeros = 0
    ones = 0
    twos = 0
    for color in nums:
        if color == 0:
            zeros += 1
        elif color == 1:
            ones += 1
        else:
            twos += 1

    write = 0
    for color, count in ((0, zeros), (1, ones), (2, twos)):
        for _ in range(count):
            nums[write] = color
            write += 1


def sort_colors_optimal(nums: list[int]) -> None:
    """Dutch national flag: O(n) time, O(1) extra space, one pass.
    Regions: [0, low) zeros, [low, scan) ones, (high, n) twos.
    The unknown region [scan, high] shrinks on every iteration.
    """
    low = scan = 0
    high = len(nums) - 1
    while scan <= high:
        if nums[scan] == 0:
            nums[low], nums[scan] = nums[scan], nums[low]
            low += 1
            scan += 1
        elif nums[scan] == 2:
            nums[scan], nums[high] = nums[high], nums[scan]
            high -= 1
            # The incoming value is still unknown; inspect it before advancing.
        else:
            scan += 1


class Solution:
    def sortColors(self, nums: list[int]) -> None:
        sort_colors_optimal(nums)


def main() -> None:
    cases = [
        ([2, 0, 2, 1, 1, 0], [0, 0, 1, 1, 2, 2]),
        ([2, 0, 1], [0, 1, 2]), ([0], [0]), ([1], [1]), ([2], [2]),
        ([2, 0], [0, 2]), ([1, 1, 1], [1, 1, 1]),
        ([0, 0, 1, 2], [0, 0, 1, 2]),
        ([2] * 100 + [1] * 100 + [0] * 100,
         [0] * 100 + [1] * 100 + [2] * 100),
    ]
    for original, expected in cases:
        for solve in (sort_colors_straightforward, sort_colors_optimal,
                      Solution().sortColors):
            nums = original.copy()
            assert solve(nums) is None
            assert nums == expected
    print('Sort Colors: all checks passed.')


if __name__ == '__main__':
    main()
