"""283. Move Zeroes — Easy.
https://leetcode.com/problems/move-zeroes/
Constraints: 1 <= len(nums) <= 10000; signed 32-bit integer values.
Both approaches mutate the original list and preserve nonzero order.
"""


def move_straightforward(nums: list[int]) -> None:
    """Shift the next nonzero into each gap. O(n**2) time, O(1) space."""
    for position in range(len(nums)):
        if nums[position] != 0:
            continue
        next_nonzero = position + 1
        while next_nonzero < len(nums) and nums[next_nonzero] == 0:
            next_nonzero += 1
        if next_nonzero == len(nums):
            break  # Only zeros remain.
        # All intervening entries are zero, so this preserves nonzero order.
        nums[position] = nums[next_nonzero]
        nums[next_nonzero] = 0


def move_optimal(nums: list[int]) -> None:
    """Stable compaction with a write pointer. O(n) time, O(1) space."""
    write = 0
    for read in range(len(nums)):
        if nums[read] != 0:
            if write != read:
                nums[write], nums[read] = nums[read], nums[write]
            write += 1
        # Before read advances, [write, read] contains only zeros.


class Solution:
    def moveZeroes(self, nums: list[int]) -> None:
        move_optimal(nums)


def main() -> None:
    from itertools import product

    solvers = (move_straightforward, move_optimal, Solution().moveZeroes)

    def check(values: list[int], expected: list[int]) -> None:
        for solve in solvers:
            nums = values.copy()
            alias = nums
            assert solve(nums) is None
            assert alias is nums and alias == expected

    check([0, 1, 0, 3, 12], [1, 3, 12, 0, 0])
    check([0], [0])
    check([0, -2**31, 0, 2**31 - 1], [-2**31, 2**31 - 1, 0, 0])
    checked = 0
    for n in range(1, 9):
        for values in product((-1, 0, 1), repeat=n):
            nums = list(values)
            expected = [x for x in nums if x != 0] + [0] * nums.count(0)
            check(nums, expected)
            checked += 1
    check([0] * 10000, [0] * 10000)
    check(list(range(1, 10001)), list(range(1, 10001)))
    check([0] * 5000 + [1] * 5000, [1] * 5000 + [0] * 5000)
    print(f"Move Zeroes: {checked} exhaustive cases, examples, and bounds passed")


if __name__ == '__main__':
    main()
