"""LeetCode 11: Container With Most Water (Medium).

https://leetcode.com/problems/container-with-most-water/
Choose two vertical lines to maximize width times the shorter line's height.
Constraints: 2 <= len(height) <= 100_000; 0 <= height[i] <= 10_000.
Neither approach changes the input. The quadratic version is for learning;
use the linear version for large inputs and interviews.
"""


def max_area_lengthy(height: list[int]) -> int:
    """Evaluate every pair of walls. Time: O(n²). Extra space: O(1)."""
    best = 0
    for left in range(len(height) - 1):
        for right in range(left + 1, len(height)):
            area = (right - left) * min(height[left], height[right])
            best = max(best, area)
    return best


def max_area_optimal(height: list[int]) -> int:
    """Move two pointers inward. Time: O(n). Extra space: O(1)."""
    left, right = 0, len(height) - 1
    best = 0
    while left < right:
        best = max(best, (right - left) * min(height[left], height[right]))
        # Keeping the shorter wall while reducing width cannot improve its area.
        # Discard that wall; with equal heights either wall can be discarded.
        if height[left] <= height[right]:
            left += 1
        else:
            right -= 1
    return best


class Solution:
    """LeetCode-compatible entry point."""

    def maxArea(self, height: list[int]) -> int:
        return max_area_optimal(height)


def main() -> None:
    cases = [([1, 8, 6, 2, 5, 4, 8, 3, 7], 49), ([1, 1], 1),
             ([0, 0], 0), ([4, 4, 4, 4], 12), ([1, 2, 3, 4, 5], 6),
             ([5, 4, 3, 2, 1], 6), ([10_000, 0, 10_000], 20_000)]
    for height, expected in cases:
        lengthy = max_area_lengthy(height)
        optimal = max_area_optimal(height)
        assert lengthy == optimal == expected, (height, lengthy, optimal)
        print(f"height={height}: lengthy={lengthy}, optimal={optimal}")


if __name__ == "__main__":
    main()
