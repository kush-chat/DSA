"""LeetCode 278: First Bad Version (Easy).

https://leetcode.com/problems/first-bad-version/
Find the first True in a monotone version predicate.
Constraints: 1 <= bad <= n <= 2**31 - 1. A bad version always exists.
The linear baseline is educational; use binary search for large n.
"""
from collections.abc import Callable


def first_bad_version_lengthy(n: int, is_bad: Callable[[int], bool]) -> int:
    """Scan versions. O(n) API calls/time, O(1) extra space."""
    for version in range(1, n + 1):
        if is_bad(version):
            return version
    raise AssertionError('A bad version must exist')


def first_bad_version_optimal(n: int, is_bad: Callable[[int], bool]) -> int:
    """Binary search. O(log n) API calls/time, O(1) extra space."""
    left, right = 1, n
    while left < right:
        middle = left + (right - left) // 2
        if is_bad(middle):
            right = middle  # This may be the first bad version: keep it.
        else:
            left = middle + 1
    return left


class Solution:
    def firstBadVersion(self, n: int) -> int:
        # LeetCode supplies this global API; local main installs a test double.
        return first_bad_version_optimal(n, isBadVersion)


def main() -> None:
    global isBadVersion
    for n, bad in [(5, 4), (1, 1), (10, 1), (10, 10), (2, 2), (9, 5)]:
        def is_bad(version: int) -> bool:
            assert 1 <= version <= n
            return version >= bad
        isBadVersion = is_bad
        lengthy = first_bad_version_lengthy(n, is_bad)
        optimal = first_bad_version_optimal(n, is_bad)
        assert lengthy == optimal == bad
        assert Solution().firstBadVersion(n) == bad
        print(f'n={n}, bad={bad}: lengthy={lengthy}, optimal={optimal}')


if __name__ == '__main__':
    main()
