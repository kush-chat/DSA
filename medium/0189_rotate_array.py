"""189. Rotate Array — Medium.
https://leetcode.com/problems/rotate-array/
Constraints: 1 <= len(nums) <= 100000; 0 <= k <= 100000;
values are signed 32-bit integers. Mutate nums to rotate right by k.
"""


def rotate_straightforward(nums: list[int], k: int) -> None:
    """Place each value in a separate result array. O(n) time and space."""
    n = len(nums)
    steps = k % n
    if steps == 0:
        return
    rotated = [0] * n
    for source in range(n):
        destination = source + steps
        if destination >= n:
            destination -= n
        rotated[destination] = nums[source]
    # Copy into the existing list so callers retaining an alias see the result.
    for index in range(n):
        nums[index] = rotated[index]


def rotate_optimal(nums: list[int], k: int) -> None:
    """Three in-place reversals. O(n) time, O(1) auxiliary space."""
    steps = k % len(nums)
    if steps == 0:
        return

    def reverse(left: int, right: int) -> None:
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1

    # Write the original as A+B where B has steps elements. Reversing all
    # gives reverse(B)+reverse(A); reversing each block restores B+A.
    reverse(0, len(nums) - 1)
    reverse(0, steps - 1)
    reverse(steps, len(nums) - 1)


class Solution:
    def rotate(self, nums: list[int], k: int) -> None:
        rotate_optimal(nums, k)


def main() -> None:
    from collections import deque
    from itertools import product

    solvers = (rotate_straightforward, rotate_optimal, Solution().rotate)

    def check(values: list[int], k: int, expected: list[int]) -> None:
        for solve in solvers:
            nums = values.copy()
            alias = nums
            assert solve(nums, k) is None
            assert alias is nums and alias == expected

    check([1, 2, 3, 4, 5, 6, 7], 3, [5, 6, 7, 1, 2, 3, 4])
    check([-1, -100, 3, 99], 2, [3, 99, -1, -100])
    check([-2**31, 2**31 - 1], 1, [2**31 - 1, -2**31])
    checked = 0
    for n in range(1, 8):
        for values in product((-1, 0, 1), repeat=n):
            for k in range(2 * n + 1):
                oracle = deque(values)
                oracle.rotate(k)
                check(list(values), k, list(oracle))
                checked += 1
    values = list(range(100000))
    for k in (0, 1, 49999, 100000):
        oracle = deque(values)
        oracle.rotate(k)
        check(values, k, list(oracle))
    check([42], 100000, [42])
    print(f"Rotate Array: {checked} exhaustive cases, examples, and bounds passed")


if __name__ == '__main__':
    main()
