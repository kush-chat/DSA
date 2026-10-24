"""LeetCode 560: Subarray Sum Equals K (Medium).

https://leetcode.com/problems/subarray-sum-equals-k/
Count nonempty contiguous subarrays whose sum is k.
Constraints: 1..20_000 elements; values -1000..1000; k -10_000_000..10_000_000.
Neither solution mutates nums. The quadratic version is educational; use the
prefix-frequency version on large inputs. Negative values rule out a general
sliding-window solution based on increasing/decreasing the sum.
"""


def subarray_sum_lengthy(nums: list[int], k: int) -> int:
    """Extend every starting position. Time: O(n²). Extra space: O(1)."""
    count = 0
    for start in range(len(nums)):
        total = 0
        for end in range(start, len(nums)):
            total += nums[end]
            if total == k:
                count += 1
    return count


def subarray_sum_optimal(nums: list[int], k: int) -> int:
    """Count matching earlier prefix sums. Expected time: O(n). Space: O(n)."""
    frequencies = {0: 1}  # Empty prefix allows subarrays beginning at index zero.
    prefix = 0
    count = 0
    for value in nums:
        prefix += value
        count += frequencies.get(prefix - k, 0)
        # Insert afterwards to avoid counting an empty subarray when k == 0.
        frequencies[prefix] = frequencies.get(prefix, 0) + 1
    return count


class Solution:
    def subarraySum(self, nums: list[int], k: int) -> int:
        return subarray_sum_optimal(nums, k)


def main() -> None:
    cases = [([1, 1, 1], 2, 2), ([1, 2, 3], 3, 2), ([0], 0, 1),
             ([0, 0, 0], 0, 6), ([1, -1, 0], 0, 3),
             ([-1, -1, 1], -1, 3), ([5], 5, 1), ([5], 0, 0),
             ([1000, -1000], 10_000_000, 0)]
    for nums, k, expected in cases:
        lengthy = subarray_sum_lengthy(nums, k)
        optimal = subarray_sum_optimal(nums, k)
        assert lengthy == optimal == expected, (nums, k, lengthy, optimal)
        print(f'{nums=}, {k=}: lengthy={lengthy}, optimal={optimal}')


if __name__ == '__main__':
    main()
