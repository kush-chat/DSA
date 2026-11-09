"""78. Subsets — Medium.
https://leetcode.com/problems/subsets/
Constraints: 1 <= len(nums) <= 10; distinct integers in [-10, 10].
Both approaches preserve the input and return independent subset lists.
"""


def subsets_straightforward(nums: list[int]) -> list[list[int]]:
    """Enumerate every membership mask and inspect all n bits.
    O(n * 2**n) time; O(n) working space, excluding O(n * 2**n) output.
    """
    result: list[list[int]] = []
    number_of_masks = 1 << len(nums)
    for mask in range(number_of_masks):
        subset: list[int] = []
        for position in range(len(nums)):
            position_bit = 1 << position
            is_selected = (mask & position_bit) != 0
            if is_selected:
                subset.append(nums[position])
        result.append(subset)
    return result


def subsets_optimal(nums: list[int]) -> list[list[int]]:
    """Backtrack over increasing indices, visiting each subset once.
    O(n * 2**n) time including copies, optimal for explicit output;
    O(n) auxiliary path/stack space, plus O(n * 2**n) output space.
    """
    result: list[list[int]] = []
    path: list[int] = []

    def visit(start: int) -> None:
        result.append(path.copy())  # Later backtracking must not change outputs.
        for index in range(start, len(nums)):
            path.append(nums[index])
            visit(index + 1)  # Increasing indices prevent duplicate subsets.
            path.pop()

    visit(0)
    return result


class Solution:
    def subsets(self, nums: list[int]) -> list[list[int]]:
        return subsets_optimal(nums)


def main() -> None:
    from itertools import combinations

    cases = [[1, 2, 3], [0], [-10, 10], [3, -1, 0], list(range(10))]
    for nums in cases:
        expected = {tuple(c) for size in range(len(nums) + 1)
                    for c in combinations(nums, size)}
        original = nums.copy()
        for solve in (subsets_straightforward, subsets_optimal, Solution().subsets):
            actual = solve(nums)
            assert len(actual) == 2 ** len(nums)
            assert {tuple(row) for row in actual} == expected
            assert len({id(row) for row in actual}) == len(actual)
            assert nums == original
    print('Subsets: all checks passed.')


if __name__ == '__main__':
    main()
