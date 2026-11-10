"""287. Find the Duplicate Number — Medium.
https://leetcode.com/problems/find-the-duplicate-number/
Constraints: len(nums) == n + 1, 1 <= n <= 100_000, values in [1, n].
Exactly one distinct value repeats, possibly more than twice.
Both approaches leave nums unchanged and use constant extra space.
"""


def duplicate_straightforward(nums: list[int]) -> int:
    """Binary search the value range using counts: O(n log n) time, O(1) space.
    Below the duplicate, count(values <= mid) <= mid. At or above it, the
    count exceeds mid: missing values cannot offset all duplicate occurrences.
    """
    low = 1
    high = len(nums) - 1
    while low < high:
        middle = low + (high - low) // 2
        count_at_most_middle = 0
        for number in nums:
            if number <= middle:
                count_at_most_middle += 1
        if count_at_most_middle > middle:
            high = middle
        else:
            low = middle + 1
    return low


def duplicate_optimal(nums: list[int]) -> int:
    """Floyd's algorithm on index -> nums[index]: O(n) time, O(1) space.
    Index 0 has no incoming edge. Its path enters a cycle whose entry has two
    incoming edges from distinct indices, so the entry is the duplicate value.
    """
    slow = fast = 0
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break

    # Reset one pointer to the start; equal-speed steps meet at the cycle entry.
    finder = 0
    while finder != slow:
        finder = nums[finder]
        slow = nums[slow]
    return finder


class Solution:
    def findDuplicate(self, nums: list[int]) -> int:
        return duplicate_optimal(nums)


def main() -> None:
    cases = [([1, 3, 4, 2, 2], 2), ([3, 1, 3, 4, 2], 3),
             ([3, 3, 3, 3, 3], 3), ([1, 1], 1), ([2, 2, 2], 2),
             ([2, 1, 1], 1), ([1, 4, 4, 2, 4], 4),
             (list(range(1, 100_001)) + [100_000], 100_000)]
    for nums, expected in cases:
        original = nums.copy()
        assert duplicate_straightforward(nums) == expected
        assert duplicate_optimal(nums) == expected
        assert Solution().findDuplicate(nums) == expected
        assert nums == original
    print('Find the Duplicate Number: all checks passed.')


if __name__ == '__main__':
    main()
