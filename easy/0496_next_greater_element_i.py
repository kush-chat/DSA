"""496. Next Greater Element I — Easy.
https://leetcode.com/problems/next-greater-element-i/
Constraints: 1 <= len(nums1) <= len(nums2) <= 1000; values in [0, 10000].
Both arrays have unique values, and nums1 is a subset of nums2.
"""
from itertools import permutations


def next_greater_straightforward(nums1: list[int], nums2: list[int]) -> list[int]:
    """Locate each query then scan its suffix: O(m*n) time, O(m) output space."""
    answer = []
    for query in nums1:
        position = 0
        while position < len(nums2):
            if nums2[position] == query:
                break
            position += 1
        following = position + 1
        greater = -1
        while following < len(nums2):
            candidate = nums2[following]
            if candidate > query:
                greater = candidate
                break  # The first greater value, not the largest, is required.
            following += 1
        answer.append(greater)
    return answer


def next_greater_optimal(nums1: list[int], nums2: list[int]) -> list[int]:
    """Decreasing stack: O(m+n) time, O(n) auxiliary space plus output."""
    pending = []
    following = {}
    for value in nums2:
        while pending and pending[-1] < value:
            following[pending.pop()] = value
        # Unresolved values are decreasing; each is pushed and popped once.
        pending.append(value)
    return [following.get(value, -1) for value in nums1]


class Solution:
    def nextGreaterElement(self, nums1: list[int], nums2: list[int]) -> list[int]:
        return next_greater_optimal(nums1, nums2)


def check(nums1, nums2, expected):
    original1, original2 = nums1[:], nums2[:]
    assert next_greater_straightforward(nums1, nums2) == expected
    assert next_greater_optimal(nums1, nums2) == expected
    assert Solution().nextGreaterElement(nums1, nums2) == expected
    assert nums1 == original1 and nums2 == original2


def main() -> None:
    check([4, 1, 2], [1, 3, 4, 2], [-1, 3, -1])
    check([2, 4], [1, 2, 3, 4], [3, -1])
    check([0], [0], [-1])
    check([0, 10000], [0, 10000], [10000, -1])
    check(list(range(1000)), list(range(1000)), list(range(1, 1000)) + [-1])
    check(list(range(1000)), list(reversed(range(1000))), [-1] * 1000)
    count = 0
    for size in range(1, 7):
        for ordering in permutations(range(size)):
            nums2 = list(ordering)
            # Reverse query order to ensure answers follow nums1, not nums2.
            nums1 = nums2[::-1]
            expected = []
            for query in nums1:
                start = nums2.index(query) + 1
                candidates = [value for value in nums2[start:] if value > query]
                expected.append(candidates[0] if candidates else -1)
            check(nums1, nums2, expected)
            count += 1
    print(f'496: examples, bounds, and {count} exhaustive permutations passed')


if __name__ == '__main__':
    main()
