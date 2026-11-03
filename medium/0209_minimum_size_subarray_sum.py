"""LeetCode 209: Minimum Size Subarray Sum (Medium).

https://leetcode.com/problems/minimum-size-subarray-sum/
Find the shortest contiguous subarray with sum at least target, or return zero.
Constraints: 1 <= target <= 10**9; 1 <= len(nums) <= 100_000;
1 <= nums[i] <= 10_000. Both solutions preserve the input.
The quadratic baseline is educational; use the optimal version for large inputs.
"""


def min_subarray_len_lengthy(target: int, nums: list[int]) -> int:
    """Try every start with a running sum. Time O(n**2), extra space O(1)."""
    best = len(nums) + 1
    for start in range(len(nums)):
        total = 0
        for end in range(start, len(nums)):
            total += nums[end]
            if total >= target:
                best = min(best, end - start + 1)
                break  # Longer subarrays from this start cannot improve it.
    return 0 if best == len(nums) + 1 else best


def min_subarray_len_optimal(target: int, nums: list[int]) -> int:
    """Expand and shrink a window. Time O(n), extra space O(1)."""
    left = total = 0
    best = len(nums) + 1
    for right, value in enumerate(nums):
        total += value
        # Positivity makes shrinking decrease the sum; negatives invalidate this.
        while total >= target:
            best = min(best, right - left + 1)
            total -= nums[left]
            left += 1
    return 0 if best == len(nums) + 1 else best


class Solution:
    def minSubArrayLen(self, target: int, nums: list[int]) -> int:
        return min_subarray_len_optimal(target, nums)


def main() -> None:
    cases = [(7, [2, 3, 1, 2, 4, 3], 2), (4, [1, 4, 4], 1),
             (11, [1] * 8, 0), (1, [1], 1), (2, [1], 0),
             (6, [1, 2, 3], 3), (5, [1, 1, 1, 5], 1),
             (10**9, [10000], 0)]
    for target, nums, expected in cases:
        before = nums[:]
        lengthy = min_subarray_len_lengthy(target, nums)
        optimal = min_subarray_len_optimal(target, nums)
        assert lengthy == optimal == expected
        assert Solution().minSubArrayLen(target, nums) == expected
        assert nums == before
        print(f'target={target}: lengthy={lengthy}, optimal={optimal}')


if __name__ == '__main__':
    main()
