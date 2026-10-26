"""LeetCode 53: Maximum Subarray (Medium).

https://leetcode.com/problems/maximum-subarray/
Return the largest sum of a nonempty contiguous subarray.
Constraints: 1..100_000 elements; values -10_000..10_000. Inputs are not mutated.
The quadratic baseline is educational; use Kadane's algorithm for large inputs.
"""


def max_subarray_lengthy(nums: list[int]) -> int:
    """Try every start and end, accumulating sums. Time: O(n²). Space: O(1)."""
    best = nums[0]
    for start in range(len(nums)):
        total = 0
        for end in range(start, len(nums)):
            total += nums[end]
            best = max(best, total)
    return best


def max_subarray_optimal(nums: list[int]) -> int:
    """Kadane's algorithm. Time: O(n). Extra space: O(1)."""
    ending_here = best = nums[0]  # Using zero would wrongly allow an empty answer.
    for index in range(1, len(nums)):
        value = nums[index]
        # A negative previous sum hurts: start fresh instead of extending it.
        ending_here = max(value, ending_here + value)
        best = max(best, ending_here)
    return best


class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        return max_subarray_optimal(nums)


def main() -> None:
    cases = [([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6), ([1], 1),
             ([5, 4, -1, 7, 8], 23), ([-8, -3, -6], -3),
             ([-10_000], -10_000), ([0, 0], 0), ([2, -3, 4], 4),
             ([4, -1, 2, 1], 6), ([10_000, 10_000], 20_000)]
    for nums, expected in cases:
        lengthy = max_subarray_lengthy(nums)
        optimal = max_subarray_optimal(nums)
        assert lengthy == optimal == expected, (nums, lengthy, optimal)
        print(f'{nums=}: lengthy={lengthy}, optimal={optimal}')


if __name__ == '__main__':
    main()
