"""LeetCode 128: Longest Consecutive Sequence (Medium).

https://leetcode.com/problems/longest-consecutive-sequence/
Find the longest run of consecutive values, regardless of input order.
Constraints: 0 <= len(nums) <= 100_000; -10**9 <= nums[i] <= 10**9.
The sorting baseline is educational; only the optimal method meets the requested
linear expected time. Both preserve the input.
"""


def longest_consecutive_lengthy(nums: list[int]) -> int:
    """Sort a copy and count runs. Time O(n log n), extra space O(n)."""
    if not nums:
        return 0
    ordered = sorted(nums)
    best = current = 1
    for index in range(1, len(ordered)):
        if ordered[index] == ordered[index - 1]:
            continue  # Duplicates neither extend nor break the current run.
        if ordered[index] == ordered[index - 1] + 1:
            current += 1
        else:
            current = 1
        best = max(best, current)
    return best


def longest_consecutive_optimal(nums: list[int]) -> int:
    """Expand only from run starts. Expected time O(n), extra space O(n)."""
    values = set(nums)
    best = 0
    # Iterate unique values so duplicate starts cannot trigger repeated scans.
    for start in values:
        if start - 1 in values:
            continue
        end = start
        while end in values:
            end += 1
        best = max(best, end - start)
    # Each distinct value is visited by the inner loop exactly once overall.
    return best


class Solution:
    def longestConsecutive(self, nums: list[int]) -> int:
        return longest_consecutive_optimal(nums)


def main() -> None:
    cases = [([100, 4, 200, 1, 3, 2], 4),
             ([0, 3, 7, 2, 5, 8, 4, 6, 0, 1], 9), ([1, 0, 1, 2], 3),
             ([], 0), ([7], 1), ([5, 5, 5], 1), ([-2, -1, 0, 2], 3),
             ([-10**9, 10**9], 1), ([9, 8, 7, 6], 4)]
    for nums, expected in cases:
        before = nums[:]
        lengthy = longest_consecutive_lengthy(nums)
        optimal = longest_consecutive_optimal(nums)
        assert lengthy == optimal == expected
        assert Solution().longestConsecutive(nums) == expected
        assert nums == before
        print(f'{nums}: lengthy={lengthy}, optimal={optimal}')


if __name__ == '__main__':
    main()
