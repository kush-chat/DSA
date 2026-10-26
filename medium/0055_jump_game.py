"""LeetCode 55: Jump Game (Medium).

https://leetcode.com/problems/jump-game/
Decide whether jumps of at most nums[i] can reach the last index from index 0.
Constraints: 1..10_000 elements; values 0..100_000. Inputs are not mutated.
The DP baseline is educational; use the greedy solution for large inputs.
"""


def can_jump_lengthy(nums: list[int]) -> bool:
    """Mark positions reachable from earlier positions. Time: O(n²). Space: O(n)."""
    reachable = [False] * len(nums)
    reachable[0] = True
    for destination in range(1, len(nums)):
        for source in range(destination):
            if reachable[source] and source + nums[source] >= destination:
                reachable[destination] = True
                break
    return reachable[-1]


def can_jump_optimal(nums: list[int]) -> bool:
    """Maintain the furthest reachable index. Time: O(n). Extra space: O(1)."""
    furthest = 0
    for index, jump in enumerate(nums):
        if index > furthest:
            return False  # No previously reachable position can cross this gap.
        furthest = max(furthest, index + jump)
        if furthest >= len(nums) - 1:
            return True
    return False


class Solution:
    def canJump(self, nums: list[int]) -> bool:
        return can_jump_optimal(nums)


def main() -> None:
    cases = [([2, 3, 1, 1, 4], True), ([3, 2, 1, 0, 4], False),
             ([0], True), ([0, 1], False), ([1, 0], True),
             ([2, 0, 0], True), ([1, 0, 1], False), ([100_000, 0, 0], True)]
    for nums, expected in cases:
        lengthy = can_jump_lengthy(nums)
        optimal = can_jump_optimal(nums)
        assert lengthy == optimal == expected, (nums, lengthy, optimal)
        print(f'{nums=}: lengthy={lengthy}, optimal={optimal}')


if __name__ == '__main__':
    main()
