"""LeetCode 217: Contains Duplicate (Easy).

https://leetcode.com/problems/contains-duplicate/
Return whether an integer occurs more than once.
Constraints: 1 <= len(nums) <= 100_000; -10**9 <= nums[i] <= 10**9.
Neither approach modifies the input.
"""


def contains_duplicate_lengthy(nums: list[int]) -> bool:
    """Sort a copy and compare neighbors. Time O(n log n), extra space O(n)."""
    ordered = sorted(nums)
    for index in range(1, len(ordered)):
        if ordered[index] == ordered[index - 1]:
            return True
    return False


def contains_duplicate_optimal(nums: list[int]) -> bool:
    """Track previous values. Expected time O(n), extra space O(n)."""
    seen: set[int] = set()
    for value in nums:
        if value in seen:
            return True
        seen.add(value)
    return False


class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        return contains_duplicate_optimal(nums)


def main() -> None:
    cases = [([1, 2, 3, 1], True), ([1, 2, 3, 4], False),
             ([1, 1, 1, 3, 3, 4, 3, 2, 4, 2], True), ([0], False),
             ([-1, 0, -1], True), ([-10**9, 10**9], False), ([2, 2], True)]
    for nums, expected in cases:
        before = nums[:]
        lengthy = contains_duplicate_lengthy(nums)
        optimal = contains_duplicate_optimal(nums)
        assert lengthy == optimal == expected
        assert Solution().containsDuplicate(nums) == expected
        assert nums == before
        print(f'{nums}: lengthy={lengthy}, optimal={optimal}')


if __name__ == '__main__':
    main()
