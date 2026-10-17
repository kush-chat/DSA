"""LeetCode 84: Largest Rectangle in Histogram (Hard).

https://leetcode.com/problems/largest-rectangle-in-histogram/
Find the largest rectangular area under consecutive bars, each of width one.
Constraints: 1 <= len(heights) <= 100_000; 0 <= heights[i] <= 10_000.
Neither solution mutates heights. Use the linear stack solution for large inputs.
"""


def largest_rectangle_lengthy(heights: list[int]) -> int:
    """Try every interval, tracking its minimum. Time: O(n²). Space: O(1)."""
    best = 0
    for left in range(len(heights)):
        shortest = heights[left]
        for right in range(left, len(heights)):
            shortest = min(shortest, heights[right])
            best = max(best, shortest * (right - left + 1))
    return best


def largest_rectangle_optimal(heights: list[int]) -> int:
    """Use an increasing stack of bar indices. Time: O(n). Space: O(n)."""
    stack: list[int] = []
    best = 0
    for right in range(len(heights) + 1):
        # A virtual final zero flushes positive bars without changing the input.
        current = heights[right] if right < len(heights) else 0
        while stack and heights[stack[-1]] > current:
            height = heights[stack.pop()]
            left = stack[-1] if stack else -1
            # The popped bar spans from left + 1 through right - 1.
            best = max(best, height * (right - left - 1))
        if right < len(heights):
            stack.append(right)
    # Each index is pushed and popped at most once, so the nested loop is linear.
    return best


class Solution:
    """LeetCode-compatible entry point."""

    def largestRectangleArea(self, heights: list[int]) -> int:
        return largest_rectangle_optimal(heights)


def main() -> None:
    cases = [([2, 1, 5, 6, 2, 3], 10), ([2, 4], 4), ([0], 0),
             ([10_000], 10_000), ([2, 2, 2], 6), ([2, 0, 2], 2),
             ([1, 2, 3, 4, 5], 9), ([5, 4, 3, 2, 1], 9),
             ([0, 0, 0], 0), ([2, 1, 2], 3)]
    for heights, expected in cases:
        lengthy = largest_rectangle_lengthy(heights)
        optimal = largest_rectangle_optimal(heights)
        assert lengthy == optimal == expected, (heights, lengthy, optimal)
        print(f"heights={heights}: lengthy={lengthy}, optimal={optimal}")


if __name__ == "__main__":
    main()
