"""169. Majority Element — Easy.
https://leetcode.com/problems/majority-element/

Constraints: 1 <= len(nums) <= 50_000; values are between -10**9 and
10**9 inclusive. A value occurring strictly more than half the time exists.
"""


def majority_straightforward(nums: list[int]) -> int:
    """Count frequencies explicitly: O(n) expected time, O(k) extra space
    for k distinct values. Does not modify the input.
    """
    counts: dict[int, int] = {}
    for number in nums:
        if number not in counts:
            counts[number] = 0
        counts[number] += 1

    threshold = len(nums) // 2
    for number, frequency in counts.items():
        if frequency > threshold:
            return number
    raise ValueError('Input must contain a strict majority.')


def majority_optimal(nums: list[int]) -> int:
    """Boyer-Moore voting: O(n) time and O(1) extra space.
    Cancelling unequal pairs cannot eliminate a strict majority. The problem's
    existence guarantee makes a separate candidate-verification pass unnecessary.
    """
    candidate = nums[0]
    balance = 0
    for number in nums:
        if balance == 0:
            candidate = number
        balance += 1 if number == candidate else -1
    return candidate


class Solution:
    def majorityElement(self, nums: list[int]) -> int:
        return majority_optimal(nums)


def main() -> None:
    cases = [
        ([3, 2, 3], 3), ([2, 2, 1, 1, 1, 2, 2], 2),
        ([7], 7), ([0, 0], 0), ([-1, 2, -1], -1),
        ([1, 2, 3, 2, 2], 2),
        ([-10**9, 10**9, 10**9], 10**9),
        ([0] * 24_999 + [1] * 25_001, 1),
    ]
    for nums, expected in cases:
        original = nums.copy()
        assert majority_straightforward(nums) == expected
        assert majority_optimal(nums) == expected
        assert Solution().majorityElement(nums) == expected
        assert nums == original
    print('Majority Element: all checks passed.')


if __name__ == '__main__':
    main()
