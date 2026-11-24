"""647. Palindromic Substrings — Medium.
https://leetcode.com/problems/palindromic-substrings/
Constraints: 1 <= len(s) <= 1000; lowercase English letters only.
"""


def count_straightforward(s: str) -> int:
    """Record every palindromic interval. O(n**2) time and auxiliary space."""
    n = len(s)
    palindrome = [[False] * n for _ in range(n)]
    total = 0
    for length in range(1, n + 1):
        for left in range(n - length + 1):
            right = left + length - 1
            if s[left] != s[right]:
                continue
            if length <= 2:
                palindrome[left][right] = True
            else:
                palindrome[left][right] = palindrome[left + 1][right - 1]
            if palindrome[left][right]:
                total += 1
    return total


def count_optimal(s: str) -> int:
    """Manacher radii for odd/even centers: O(n) time and auxiliary space."""
    n = len(s)
    odd = [0] * n
    left, right = 0, -1
    for center in range(n):
        # Reuse the reflected radius, clipped to the known right boundary.
        radius = 1 if center > right else min(odd[left + right - center], right - center + 1)
        while center - radius >= 0 and center + radius < n and s[center - radius] == s[center + radius]:
            radius += 1
        odd[center] = radius
        if center + radius - 1 > right:
            left, right = center - radius + 1, center + radius - 1

    even = [0] * n
    left, right = 0, -1
    for center in range(n):
        # The even center lies between center-1 and center.
        radius = 0 if center > right else min(even[left + right - center + 1], right - center + 1)
        while center - radius - 1 >= 0 and center + radius < n and s[center - radius - 1] == s[center + radius]:
            radius += 1
        even[center] = radius
        if center + radius - 1 > right:
            left, right = center - radius, center + radius - 1
    # Each radius counts the nested palindromes with that unique center.
    # Expansions beyond a reused interval advance right, so total work is linear.
    return sum(odd) + sum(even)


class Solution:
    def countSubstrings(self, s: str) -> int:
        return count_optimal(s)


def main() -> None:
    from itertools import product

    cases = [("abc", 3), ("aaa", 6), ("a", 1), ("abba", 6),
             ("ababa", 9), ("aaaa", 10)]
    for s, expected in cases:
        assert count_straightforward(s) == expected
        assert count_optimal(s) == expected
        assert Solution().countSubstrings(s) == expected
    checked = 0
    for n in range(1, 9):
        for letters in product("abc", repeat=n):
            s = "".join(letters)
            expected = sum(s[a:b] == s[a:b][::-1]
                           for a in range(n) for b in range(a + 1, n + 1))
            assert count_straightforward(s) == expected
            assert count_optimal(s) == expected
            checked += 1
    for solve in (count_straightforward, count_optimal):
        assert solve("a" * 1000) == 500500
        assert solve("ab" * 500) == 250500
        assert solve("a" * 500 + "b" * 500) == 250500
    print(f"Palindromic Substrings: {checked} exhaustive cases and bounds passed")


if __name__ == '__main__':
    main()
