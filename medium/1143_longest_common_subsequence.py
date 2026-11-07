"""1143. Longest Common Subsequence — Medium.
https://leetcode.com/problems/longest-common-subsequence/

Constraints: 1 <= len(text1), len(text2) <= 1000; lowercase English letters.
Both implementations also support empty strings as a useful extension.
"""


def lcs_straightforward(text1: str, text2: str) -> int:
    """Full prefix table: O(m*n) time and O(m*n) extra space.
    table[i][j] is the LCS length of text1[:i] and text2[:j].
    """
    rows, columns = len(text1), len(text2)
    table = [[0] * (columns + 1) for _ in range(rows + 1)]
    for i in range(1, rows + 1):
        for j in range(1, columns + 1):
            if text1[i - 1] == text2[j - 1]:
                # Equal final letters extend an optimal pair of shorter prefixes.
                table[i][j] = table[i - 1][j - 1] + 1
            else:
                # At least one of the unequal final letters must be omitted.
                omit_first = table[i - 1][j]
                omit_second = table[i][j - 1]
                table[i][j] = max(omit_first, omit_second)
    return table[rows][columns]


def lcs_optimal(text1: str, text2: str) -> int:
    """Space-optimized interview DP: O(m*n) time, O(min(m,n)) extra space.
    Keep the shorter string along the columns; retain the overwritten diagonal.
    """
    if len(text1) < len(text2):
        text1, text2 = text2, text1
    lengths = [0] * (len(text2) + 1)
    for first in text1:
        diagonal = 0
        for j, second in enumerate(text2, start=1):
            above = lengths[j]  # Previous row, before overwriting it.
            if first == second:
                lengths[j] = diagonal + 1
            else:
                lengths[j] = max(above, lengths[j - 1])
            diagonal = above
    return lengths[-1]


class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        return lcs_optimal(text1, text2)


def main() -> None:
    cases = [
        ("abcde", "ace", 3), ("abc", "abc", 3), ("abc", "def", 0),
        ("a", "a", 1), ("a", "b", 0), ("aaaa", "aa", 2),
        ("abc", "cba", 1), ("abcbdab", "bdcaba", 4),
        ("", "abc", 0), ("abc", "", 0),
        ("a" * 1000, "a" * 1000, 1000),
        ("a" * 1000, "b" * 1000, 0),
    ]
    for first, second, expected in cases:
        assert lcs_straightforward(first, second) == expected
        assert lcs_optimal(first, second) == expected
        assert Solution().longestCommonSubsequence(first, second) == expected
    print("Longest Common Subsequence: all checks passed.")


if __name__ == '__main__':
    main()
