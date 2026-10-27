"""LeetCode 136: Single Number (Easy).

https://leetcode.com/problems/single-number/
Find the sole value occurring once; every other value occurs exactly twice.
Constraints: 1..30_000 elements; values -30_000..30_000. Input is not mutated.
Only the XOR version meets the required constant-extra-space bound.
"""


def single_number_lengthy(nums: list[int]) -> int:
    """Count occurrences. Expected time: O(n). Extra space: O(n)."""
    counts: dict[int, int] = {}
    for value in nums:
        counts[value] = counts.get(value, 0) + 1
    for value, count in counts.items():
        if count == 1:
            return value
    raise ValueError('Input must contain a single unpaired value')


def single_number_optimal(nums: list[int]) -> int:
    """Cancel pairs using XOR. Time: O(n). Extra space: O(1)."""
    result = 0
    for value in nums:
        # x ^ x == 0 and x ^ 0 == x; ordering does not affect cancellation.
        result ^= value
    return result


class Solution:
    def singleNumber(self, nums: list[int]) -> int:
        return single_number_optimal(nums)


def main() -> None:
    cases = [([2, 2, 1], 1), ([4, 1, 2, 1, 2], 4), ([1], 1),
             ([0], 0), ([-3, 0, -3], 0), ([0, -30000, 0], -30000)]
    for nums, expected in cases:
        lengthy = single_number_lengthy(nums)
        optimal = single_number_optimal(nums)
        assert lengthy == optimal == expected
        print(f'{nums=}: lengthy={lengthy}, optimal={optimal}')


if __name__ == '__main__':
    main()
