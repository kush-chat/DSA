"""LeetCode 238: Product of Array Except Self (Medium).

https://leetcode.com/problems/product-of-array-except-self/
Return the product of every element except the one at each output index.
Constraints: 2..100_000 elements; values -30..30; all prefix, suffix, and
answer products fit in signed 32-bit integers. Neither solution uses division
or mutates nums. Both run in O(n); the optimal version reduces extra storage.
"""


def product_except_self_lengthy(nums: list[int]) -> list[int]:
    """Build separate prefix/suffix tables. Time: O(n). Extra space: O(n)."""
    n = len(nums)
    prefix = [1] * n
    suffix = [1] * n
    for index in range(1, n):
        prefix[index] = prefix[index - 1] * nums[index - 1]
    for index in range(n - 2, -1, -1):
        suffix[index] = suffix[index + 1] * nums[index + 1]
    answer = []
    for index in range(n):
        answer.append(prefix[index] * suffix[index])
    return answer


def product_except_self_optimal(nums: list[int]) -> list[int]:
    """Reuse output for prefixes. Time: O(n). Extra space: O(1), excluding output."""
    answer = [1] * len(nums)
    prefix = 1
    for index, value in enumerate(nums):
        answer[index] = prefix
        prefix *= value
    suffix = 1
    for index in range(len(nums) - 1, -1, -1):
        # Multiply by the product strictly to the right, then include this value.
        answer[index] *= suffix
        suffix *= nums[index]
    return answer


class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        return product_except_self_optimal(nums)


def main() -> None:
    cases = [([1, 2, 3, 4], [24, 12, 8, 6]),
             ([-1, 1, 0, -3, 3], [0, 0, 9, 0, 0]),
             ([0, 0], [0, 0]), ([0, 5], [5, 0]), ([5, 0], [0, 5]),
             ([-2, 3], [3, -2]), ([-1, -2, -3], [6, 3, 2]),
             ([1, 1, 1], [1, 1, 1])]
    for nums, expected in cases:
        lengthy = product_except_self_lengthy(nums)
        optimal = product_except_self_optimal(nums)
        assert lengthy == optimal == expected, (nums, lengthy, optimal)
        print(f'{nums=}: lengthy={lengthy}, optimal={optimal}')


if __name__ == '__main__':
    main()
