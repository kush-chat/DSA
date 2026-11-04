"""LeetCode 674: Longest Continuous Increasing Subsequence (Easy).

https://leetcode.com/problems/longest-continuous-increasing-subsequence/
Return the longest strictly increasing contiguous run length; no skipping.
Constraints: 1 <= len(nums) <= 10_000; -10**9 <= nums[i] <= 10**9.
Both solutions preserve the input.
"""


def find_length_of_lcis_lengthy(nums: list[int]) -> int:
    """Store the run length ending at every index. Time O(n), space O(n)."""
    lengths = [1] * len(nums)
    for index in range(1, len(nums)):
        if nums[index] > nums[index - 1]:
            lengths[index] = lengths[index - 1] + 1
        else:
            lengths[index] = 1
    best = 0
    for length in lengths:
        best = max(best, length)
    return best


def find_length_of_lcis_optimal(nums: list[int]) -> int:
    """Keep only the current run and best length. Time O(n), space O(1)."""
    if not nums:
        return 0
    current = best = 1
    for index in range(1, len(nums)):
        if nums[index] > nums[index - 1]:
            current += 1
        else:
            current = 1  # Equality also breaks a strictly increasing run.
        best = max(best, current)
    return best


class Solution:
    def findLengthOfLCIS(self, nums: list[int]) -> int:
        return find_length_of_lcis_optimal(nums)


def main() -> None:
    cases = [([1, 3, 5, 4, 7], 3), ([2] * 5, 1), ([9], 1),
             ([4, 3, 2, 1], 1), ([-10**9, 0, 10**9], 3),
             ([1, 2, 2, 3, 4], 3), ([1, 2, 3, 0], 3),
             ([9, 1, 2, 3, 4], 4)]
    for nums, expected in cases:
        before = nums[:]
        lengthy = find_length_of_lcis_lengthy(nums)
        optimal = find_length_of_lcis_optimal(nums)
        assert lengthy == optimal == expected
        assert Solution().findLengthOfLCIS(nums) == expected
        assert nums == before
        print(f'{nums}: lengthy={lengthy}, optimal={optimal}')


if __name__ == '__main__':
    main()
