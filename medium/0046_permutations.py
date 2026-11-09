"""46. Permutations — Medium.
https://leetcode.com/problems/permutations/
Constraints: 1 <= len(nums) <= 6; distinct integers in [-10, 10].
Both approaches preserve the input and return independent permutation lists.
"""


def permutations_straightforward(nums: list[int]) -> list[list[int]]:
    """Insert each new value at every position of every existing permutation.
    O(n * n!) time; O(n * n!) peak space including intermediate/output lists.
    """
    permutations: list[list[int]] = [[]]
    for number in nums:
        expanded: list[list[int]] = []
        for previous in permutations:
            for insertion_position in range(len(previous) + 1):
                candidate: list[int] = []
                for index in range(insertion_position):
                    candidate.append(previous[index])
                candidate.append(number)
                for index in range(insertion_position, len(previous)):
                    candidate.append(previous[index])
                expanded.append(candidate)
        permutations = expanded
    return permutations


def permutations_optimal(nums: list[int]) -> list[list[int]]:
    """Fix one position at a time by swapping candidates into it.
    O(n * n!) time (optimal for explicit output), O(n) auxiliary working/stack
    space, plus O(n * n!) output space.
    """
    working = nums.copy()
    result: list[list[int]] = []

    def visit(start: int) -> None:
        if start == len(working):
            result.append(working.copy())
            return
        for chosen in range(start, len(working)):
            working[start], working[chosen] = working[chosen], working[start]
            visit(start + 1)
            # Restore the suffix before trying the next candidate.
            working[start], working[chosen] = working[chosen], working[start]

    visit(0)
    return result


class Solution:
    def permute(self, nums: list[int]) -> list[list[int]]:
        return permutations_optimal(nums)


def main() -> None:
    from itertools import permutations
    from math import factorial

    cases = [[1, 2, 3], [0, 1], [1], [-10, 10], [2, -1, 0], list(range(6))]
    for nums in cases:
        expected = set(permutations(nums))
        original = nums.copy()
        for solve in (permutations_straightforward, permutations_optimal,
                      Solution().permute):
            actual = solve(nums)
            assert len(actual) == factorial(len(nums))
            assert {tuple(row) for row in actual} == expected
            assert len({id(row) for row in actual}) == len(actual)
            assert nums == original
    print('Permutations: all checks passed.')


if __name__ == '__main__':
    main()
