"""LeetCode 42: Trapping Rain Water (Hard).

https://leetcode.com/problems/trapping-rain-water/
Count trapped water above unit-width bars.
Constraints: 1..20_000 bars; heights 0..100_000. Neither solution mutates input.
"""


def trap_lengthy(height: list[int]) -> int:
    """Precompute the tallest walls on both sides. Time: O(n). Space: O(n)."""
    n = len(height)
    left_max = [0] * n
    right_max = [0] * n
    left_max[0] = height[0]
    right_max[-1] = height[-1]
    for index in range(1, n):
        left_max[index] = max(left_max[index - 1], height[index])
    for index in range(n - 2, -1, -1):
        right_max[index] = max(right_max[index + 1], height[index])
    water = 0
    for index in range(n):
        water += min(left_max[index], right_max[index]) - height[index]
    return water


def trap_optimal(height: list[int]) -> int:
    """Resolve the side with the smaller known wall. Time: O(n). Space: O(1)."""
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    water = 0
    while left <= right:
        # A wall at least as high is already known on the opposite side.
        # Thus the smaller running maximum determines this side's water level.
        if left_max <= right_max:
            left_max = max(left_max, height[left])
            water += left_max - height[left]
            left += 1
        else:
            right_max = max(right_max, height[right])
            water += right_max - height[right]
            right -= 1
    return water


class Solution:
    def trap(self, height: list[int]) -> int:
        return trap_optimal(height)


def main() -> None:
    cases = [([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6),
             ([4, 2, 0, 3, 2, 5], 9), ([0], 0), ([3, 3], 0),
             ([3, 0, 3], 3), ([3, 0, 0, 3], 6), ([2, 2, 2], 0),
             ([1, 2, 3, 4], 0), ([4, 3, 2, 1], 0), ([5, 0, 1], 1)]
    for heights, expected in cases:
        lengthy = trap_lengthy(heights)
        optimal = trap_optimal(heights)
        assert lengthy == optimal == expected, (heights, lengthy, optimal)
        print(f'{heights=}: lengthy={lengthy}, optimal={optimal}')


if __name__ == '__main__':
    main()
