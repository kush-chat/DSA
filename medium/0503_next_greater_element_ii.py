"""503. Next Greater Element II — Medium.
https://leetcode.com/problems/next-greater-element-ii/
Constraints: 1 <= len(nums) <= 10000; -10**9 <= nums[i] <= 10**9.
Search circularly for the first strictly greater value; duplicates are allowed.
"""
from itertools import product


def next_greater_straightforward(nums: list[int]) -> list[int]:
    """Scan at most n-1 successors per index: O(n**2) time, O(n) output space."""
    length = len(nums)
    answer = [-1] * length
    for start in range(length):
        position = start + 1
        if position == length:
            position = 0
        examined = 0
        while examined < length - 1:
            candidate = nums[position]
            if candidate > nums[start]:
                answer[start] = candidate
                break
            position += 1
            if position == length:
                position = 0
            examined += 1
    return answer


def next_greater_optimal(nums: list[int]) -> list[int]:
    """Two virtual passes with a monotonic stack: O(n) time and space."""
    length = len(nums)
    answer = [-1] * length
    pending = []
    for step in range(2 * length):
        index = step % length
        while pending and nums[pending[-1]] < nums[index]:
            answer[pending.pop()] = nums[index]
        # Store indices (not values) because equal values have distinct positions.
        # Only the first pass pushes; the second resolves wraparound successors.
        if step < length:
            pending.append(index)
    return answer


class Solution:
    def nextGreaterElements(self, nums: list[int]) -> list[int]:
        return next_greater_optimal(nums)


def check(nums, expected):
    original = nums[:]
    assert next_greater_straightforward(nums) == expected
    assert next_greater_optimal(nums) == expected
    assert Solution().nextGreaterElements(nums) == expected
    assert nums == original


def rotation_oracle(nums):
    result = []
    for i, value in enumerate(nums):
        successors = nums[i+1:] + nums[:i]
        greater = [candidate for candidate in successors if candidate > value]
        result.append(greater[0] if greater else -1)
    return result


def main() -> None:
    check([1, 2, 1], [2, -1, 2])
    check([1, 2, 3, 4, 3], [2, 3, 4, -1, 4])
    check([7], [-1])
    check([2, 2, 2], [-1, -1, -1])
    check([3, 2, 1], [-1, 3, 3])
    check([-10**9, -1, 10**9], [-1, 10**9, -1])
    check([5, 1, 5, 2], [-1, 5, -1, 5])
    # Maximum length, including a final element that has no greater successor.
    check(list(range(10000)), list(range(1, 10000)) + [-1])
    count = 0
    for size in range(1, 9):
        for values in product((-1, 0, 1), repeat=size):
            nums = list(values)
            check(nums, rotation_oracle(nums))
            count += 1
    print(f'503: examples, bounds, and {count} exhaustive arrays passed')


if __name__ == '__main__':
    main()
