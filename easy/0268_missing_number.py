"""268. Missing Number — Easy.
https://leetcode.com/problems/missing-number/

Constraints: 1 <= n <= 10**4; n distinct values from [0, n].
"""


def missing_number_straightforward(nums: list[int]) -> int:
    """Mark a presence table, then find its gap. O(n) time and space."""
    n = len(nums)
    present = [False] * (n + 1)
    for value in nums:
        present[value] = True

    # Include n itself: the absent value need not occur between two inputs.
    for candidate in range(n + 1):
        if not present[candidate]:
            return candidate
    raise ValueError("Expected exactly one missing value")


def missing_number_optimal(nums: list[int]) -> int:
    """Cancel equal values with XOR. O(n) time, O(1) auxiliary space."""
    missing = len(nums)
    for index, value in enumerate(nums):
        # All indices 0..n-1 plus the initial n form the complete range.
        # Every present value cancels; the unpaired missing value remains.
        missing ^= index ^ value
    return missing


class Solution:
    def missingNumber(self, nums: list[int]) -> int:
        return missing_number_optimal(nums)


def main() -> None:
    from itertools import permutations

    cases = [([3, 0, 1], 2), ([0, 1], 2),
             ([9, 6, 4, 2, 3, 5, 7, 0, 1], 8), ([0], 1), ([1], 0)]
    for solve in (missing_number_straightforward, missing_number_optimal):
        for nums, expected in cases:
            original = nums.copy()
            assert solve(nums) == expected
            assert nums == original

    checked = 0
    # Generate the answer first, then every ordering of the remaining values.
    for n in range(1, 7):
        for absent in range(n + 1):
            values = [v for v in range(n + 1) if v != absent]
            for ordering in permutations(values):
                nums = list(ordering)
                assert missing_number_straightforward(nums) == absent
                assert missing_number_optimal(nums) == absent
                checked += 1
    for absent in (0, 5000, 10000):
        nums = [v for v in range(10000, -1, -1) if v != absent]
        assert missing_number_straightforward(nums) == absent
        assert missing_number_optimal(nums) == absent
        assert Solution().missingNumber(nums) == absent
    print(f"Missing Number: examples, {checked} exhaustive cases, and bounds passed")


if __name__ == '__main__':
    main()
