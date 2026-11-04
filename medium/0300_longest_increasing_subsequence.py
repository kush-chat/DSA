"""LeetCode 300: Longest Increasing Subsequence (Medium).

https://leetcode.com/problems/longest-increasing-subsequence/
Return the longest strictly increasing subsequence length; skipping is allowed.
Constraints: 1 <= len(nums) <= 2500; -10_000 <= nums[i] <= 10_000.
Both solutions preserve the input.
"""
from bisect import bisect_left


def length_of_lis_lengthy(nums: list[int]) -> int:
    """DP over every earlier endpoint. Time O(n**2), extra space O(n)."""
    lengths = [1] * len(nums)
    for end in range(len(nums)):
        for previous in range(end):
            if nums[previous] < nums[end]:
                lengths[end] = max(lengths[end], lengths[previous] + 1)
    return max(lengths, default=0)


def length_of_lis_optimal(nums: list[int]) -> int:
    """Minimum tails with binary search. Time O(n log n), extra space O(n)."""
    tails: list[int] = []
    for value in nums:
        # tails[i] is the smallest possible tail of a length-(i+1) subsequence.
        # bisect_left replaces equal values: duplicates must not extend the LIS.
        position = bisect_left(tails, value)
        if position == len(tails):
            tails.append(value)
        else:
            tails[position] = value
    # tails need not itself be a subsequence; only its length is the answer.
    return len(tails)


class Solution:
    def lengthOfLIS(self, nums: list[int]) -> int:
        return length_of_lis_optimal(nums)


def main() -> None:
    cases = [([10, 9, 2, 5, 3, 7, 101, 18], 4), ([0, 1, 0, 3, 2, 3], 4),
             ([7] * 7, 1), ([1], 1), ([5, 4, 3, 2, 1], 1),
             ([-10000, 0, 10000], 3), ([1, 3, 5, 4, 7], 4),
             ([2, 2, 3, 3], 2)]
    for nums, expected in cases:
        before = nums[:]
        lengthy = length_of_lis_lengthy(nums)
        optimal = length_of_lis_optimal(nums)
        assert lengthy == optimal == expected
        assert Solution().lengthOfLIS(nums) == expected
        assert nums == before
        print(f'{nums}: lengthy={lengthy}, optimal={optimal}')


if __name__ == '__main__':
    main()
