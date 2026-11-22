"""213. House Robber II — Medium.
https://leetcode.com/problems/house-robber-ii/

Constraints: 1 <= len(nums) <= 100; 0 <= nums[i] <= 1000.
Houses form a circle, so the first and last cannot both be selected.
"""


def rob_straightforward(nums: list[int]) -> int:
    """Two explicit prefix DP tables. O(n) time and O(n) extra space."""
    n = len(nums)
    if n == 1:
        return nums[0]

    # Every valid choice omits the first or the last (possibly both).
    without_last = nums[:-1]
    without_first = nums[1:]
    answers = []
    for houses in (without_last, without_first):
        best = [0] * (len(houses) + 1)
        best[1] = houses[0]
        for count in range(2, len(houses) + 1):
            skip_current = best[count - 1]
            take_current = best[count - 2] + houses[count - 1]
            best[count] = max(skip_current, take_current)
        answers.append(best[-1])
    return max(answers)


def rob_optimal(nums: list[int]) -> int:
    """Two linear interval scans. O(n) time, O(1) auxiliary space."""
    n = len(nums)
    if n == 1:
        return nums[0]

    def rob_interval(start: int, stop: int) -> int:
        two_back = 0
        one_back = 0
        for index in range(start, stop):
            # The two previous prefix optima are all the recurrence needs.
            current = max(one_back, two_back + nums[index])
            two_back, one_back = one_back, current
        return one_back

    # Index ranges avoid allocating slices in the constant-space solution.
    return max(rob_interval(0, n - 1), rob_interval(1, n))


class Solution:
    def rob(self, nums: list[int]) -> int:
        return rob_optimal(nums)


def main() -> None:
    from itertools import product

    cases = [([2, 3, 2], 3), ([1, 2, 3, 1], 4), ([1, 2, 3], 3),
             ([0], 0), ([1000], 1000), ([2, 9], 9), ([0, 0, 0], 0),
             ([10, 1, 1, 10], 11)]
    for solve in (rob_straightforward, rob_optimal):
        for nums, expected in cases:
            original = nums.copy()
            assert solve(nums) == expected
            assert nums == original

    checked = 0
    for n in range(1, 9):
        # Independent oracle: enumerate all legal sets of houses in the circle.
        legal_sets = []
        for mask in range(1 << n):
            if n > 1 and any((mask >> i & 1) and
                             (mask >> ((i + 1) % n) & 1) for i in range(n)):
                continue
            legal_sets.append([i for i in range(n) if mask >> i & 1])
        for values in product(range(3), repeat=n):
            nums = list(values)
            expected = max(sum(nums[i] for i in chosen) for chosen in legal_sets)
            assert rob_straightforward(nums) == expected
            assert rob_optimal(nums) == expected
            checked += 1
    for nums, expected in [([1000] * 100, 50000), ([1000] * 99, 49000),
                           ([0] * 100, 0)]:
        assert rob_straightforward(nums) == expected
        assert rob_optimal(nums) == expected
        assert Solution().rob(nums) == expected
    print(f"House Robber II: examples, {checked} exhaustive cases, and bounds passed")


if __name__ == '__main__':
    main()
