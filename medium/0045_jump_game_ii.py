"""45. Jump Game II — Medium.
https://leetcode.com/problems/jump-game-ii/
Constraints: 1 <= len(nums) <= 10_000; 0 <= nums[i] <= 1000;
the last index is reachable. Neither solution modifies nums.
"""


def jumps_straightforward(nums: list[int]) -> int:
    """Relax every reachable forward jump using a DP table.
    O(n * min(n, M+1)) time for maximum jump M, O(n) extra space.
    """
    n = len(nums)
    unreachable = n + 1
    minimum = [unreachable] * n
    minimum[0] = 0
    for start in range(n):
        if minimum[start] == unreachable:
            continue
        last_destination = min(n - 1, start + nums[start])
        candidate_jumps = minimum[start] + 1
        for destination in range(start + 1, last_destination + 1):
            if candidate_jumps < minimum[destination]:
                minimum[destination] = candidate_jumps
    return minimum[-1]


def jumps_optimal(nums: list[int]) -> int:
    """Scan breadth-first reachability layers: O(n) time, O(1) extra space.
    Every index through layer_end is reachable with the current jump count.
    """
    jumps = 0
    layer_end = 0
    farthest = 0
    for index in range(len(nums) - 1):  # No departure needed from the last index.
        farthest = max(farthest, index + nums[index])
        if index == layer_end:
            jumps += 1
            layer_end = farthest
            if layer_end >= len(nums) - 1:
                break
    return jumps


class Solution:
    def jump(self, nums: list[int]) -> int:
        return jumps_optimal(nums)


def main() -> None:
    cases = [([2, 3, 1, 1, 4], 2), ([2, 3, 0, 1, 4], 2),
             ([0], 0), ([1, 0], 1), ([2, 0, 0], 1),
             ([1, 2, 1, 1, 1], 3), ([1] * 10_000, 9999),
             ([1000] * 10_000, 10)]
    for nums, expected in cases:
        original = nums.copy()
        assert jumps_straightforward(nums) == expected
        assert jumps_optimal(nums) == expected
        assert Solution().jump(nums) == expected
        assert nums == original
    print('Jump Game II: all checks passed.')


if __name__ == '__main__':
    main()
