"""LeetCode 239: Sliding Window Maximum (Hard).

https://leetcode.com/problems/sliding-window-maximum/
Return the maximum of each consecutive window of k elements.
Constraints: 1 <= k <= len(nums) <= 100_000; -10_000 <= nums[i] <= 10_000.
Both solutions preserve the input. The baseline is educational for large k.
"""
from collections import deque


def max_sliding_window_lengthy(nums: list[int], k: int) -> list[int]:
    """Scan every window. Time O((n-k+1)*k), O(1) space excluding output."""
    result = []
    for start in range(len(nums) - k + 1):
        largest = nums[start]
        for index in range(start + 1, start + k):
            largest = max(largest, nums[index])
        result.append(largest)
    return result


def max_sliding_window_optimal(nums: list[int], k: int) -> list[int]:
    """Monotonic deque. Time O(n), O(k) extra space excluding output."""
    candidates: deque[int] = deque()
    result = []
    for right, value in enumerate(nums):
        # Indices make expiry unambiguous even when values repeat.
        while candidates and candidates[0] <= right - k:
            candidates.popleft()
        # A newer value at least as large dominates an older candidate.
        while candidates and nums[candidates[-1]] <= value:
            candidates.pop()
        candidates.append(right)
        if right >= k - 1:
            result.append(nums[candidates[0]])
    # Each index enters once and leaves at most once: total deque work is linear.
    return result


class Solution:
    def maxSlidingWindow(self, nums: list[int], k: int) -> list[int]:
        return max_sliding_window_optimal(nums, k)


def main() -> None:
    cases = [([1, 3, -1, -3, 5, 3, 6, 7], 3, [3, 3, 5, 5, 6, 7]),
             ([1], 1, [1]), ([2, 2, 2], 2, [2, 2]),
             ([4, 3, 2, 1], 2, [4, 3, 2]), ([1, 2, 3, 4], 2, [2, 3, 4]),
             ([-4, -2, -3], 2, [-2, -2]), ([9, 1, 2], 3, [9]),
             ([3, -1, 2], 1, [3, -1, 2]), ([5, 1, 5, 1], 2, [5, 5, 5])]
    for nums, k, expected in cases:
        before = nums[:]
        lengthy = max_sliding_window_lengthy(nums, k)
        optimal = max_sliding_window_optimal(nums, k)
        assert lengthy == optimal == expected
        assert Solution().maxSlidingWindow(nums, k) == expected
        assert nums == before
        print(f'k={k}: lengthy={lengthy}, optimal={optimal}')


if __name__ == '__main__':
    main()
