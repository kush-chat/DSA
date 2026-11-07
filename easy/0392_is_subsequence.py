"""392. Is Subsequence — Easy.
https://leetcode.com/problems/is-subsequence/

Constraints: 0 <= len(s) <= 100; 0 <= len(t) <= 10_000;
both strings contain only lowercase English letters.
"""


def is_subsequence_straightforward(s: str, t: str) -> bool:
    """Track which prefixes of s can be formed. O(len(s)*len(t)) time,
    O(len(s)) extra space. Each row describes one more character of t.
    """
    possible = [False] * (len(s) + 1)
    possible[0] = True  # Deleting everything always produces the empty prefix.
    for character in t:
        next_possible = possible.copy()  # We can skip this character.
        for prefix_length in range(1, len(s) + 1):
            if s[prefix_length - 1] == character:
                if possible[prefix_length - 1]:
                    next_possible[prefix_length] = True
        possible = next_possible
    return possible[len(s)]


def is_subsequence_optimal(s: str, t: str) -> bool:
    """Greedily match the earliest available character: O(len(t)) time,
    O(1) extra space. Earlier matches leave at least as much room for the rest.
    """
    if not s:
        return True
    matched = 0
    for character in t:
        if s[matched] == character:
            matched += 1
            if matched == len(s):
                return True
    return False


class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        return is_subsequence_optimal(s, t)


def main() -> None:
    cases = [
        ("abc", "ahbgdc", True), ("axc", "ahbgdc", False),
        ("", "", True), ("", "abc", True), ("a", "", False),
        ("aa", "a", False), ("aaa", "aaaa", True),
        ("ba", "ab", False), ("abc", "abc", True),
        ("a" * 100, "a" * 10_000, True),
        ("a" * 99 + "b", "a" * 10_000, False),
    ]
    for s, t, expected in cases:
        assert is_subsequence_straightforward(s, t) == expected
        assert is_subsequence_optimal(s, t) == expected
        assert Solution().isSubsequence(s, t) == expected
    print("Is Subsequence: all checks passed.")


if __name__ == '__main__':
    main()
