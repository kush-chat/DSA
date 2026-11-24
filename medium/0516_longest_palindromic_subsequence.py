"""516. Longest Palindromic Subsequence — Medium.
https://leetcode.com/problems/longest-palindromic-subsequence/
Constraints: 1 <= len(s) <= 1000; lowercase English letters only.
"""


def longest_straightforward(s: str) -> int:
    """Full interval DP table: O(n**2) time and auxiliary space."""
    n = len(s)
    best = [[0] * n for _ in range(n)]
    for index in range(n):
        best[index][index] = 1
    for length in range(2, n + 1):
        for left in range(n - length + 1):
            right = left + length - 1
            if s[left] == s[right]:
                interior = best[left + 1][right - 1] if length > 2 else 0
                best[left][right] = interior + 2
            else:
                # At least one unequal endpoint must be excluded.
                without_left = best[left + 1][right]
                without_right = best[left][right - 1]
                best[left][right] = max(without_left, without_right)
    return best[0][n - 1]


def longest_optimal(s: str) -> int:
    """Compress the interval DP: O(n**2) time, O(n) auxiliary space."""
    n = len(s)
    best = [0] * n
    for left in range(n - 1, -1, -1):
        diagonal = 0  # Empty interval before processing the adjacent pair.
        best[left] = 1
        for right in range(left + 1, n):
            previous_row = best[right]  # Value for [left+1, right].
            if s[left] == s[right]:
                best[right] = diagonal + 2
            else:
                best[right] = max(best[right], best[right - 1])
            diagonal = previous_row
    return best[-1]


class Solution:
    def longestPalindromeSubseq(self, s: str) -> int:
        return longest_optimal(s)


def main() -> None:
    from itertools import product

    cases = [("bbbab", 4), ("cbbd", 2), ("a", 1), ("abc", 1),
             ("aaaa", 4), ("agbdba", 5)]
    for s, expected in cases:
        assert longest_straightforward(s) == expected
        assert longest_optimal(s) == expected
        assert Solution().longestPalindromeSubseq(s) == expected
    checked = 0
    for n in range(1, 9):
        for letters in product("ab", repeat=n):
            s = "".join(letters)
            expected = 0
            # Enumerate subsequences independently of either DP recurrence.
            for mask in range(1, 1 << n):
                candidate = "".join(s[i] for i in range(n) if mask >> i & 1)
                if candidate == candidate[::-1]:
                    expected = max(expected, len(candidate))
            assert longest_straightforward(s) == expected
            assert longest_optimal(s) == expected
            checked += 1
    for solve in (longest_straightforward, longest_optimal):
        assert solve("a" * 1000) == 1000
        assert solve("ab" * 500) == 999
        assert solve("a" * 500 + "b" * 500) == 500
    print(f"Longest Palindromic Subsequence: {checked} exhaustive cases and bounds passed")


if __name__ == '__main__':
    main()
