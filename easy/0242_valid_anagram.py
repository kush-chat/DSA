"""LeetCode 242: Valid Anagram (Easy).

https://leetcode.com/problems/valid-anagram/
Determine whether two strings contain the same letters with the same counts.
Constraints: lengths 1..50_000; lowercase English letters only.
For the Unicode follow-up, replace the 26 counters with a character dictionary.
"""


def is_anagram_lengthy(s: str, t: str) -> bool:
    """Sort and compare. Time: O(n log n). Extra space: O(n), for equal lengths."""
    if len(s) != len(t):
        return False
    sorted_s = sorted(s)
    sorted_t = sorted(t)
    for index in range(len(sorted_s)):
        if sorted_s[index] != sorted_t[index]:
            return False
    return True


def is_anagram_optimal(s: str, t: str) -> bool:
    """Balance 26 letter counts. Time: O(n). Extra space: O(1)."""
    if len(s) != len(t):
        return False
    counts = [0] * 26
    for first, second in zip(s, t):
        counts[ord(first) - ord('a')] += 1
        counts[ord(second) - ord('a')] -= 1
    # Every letter must have equal multiplicity, not just occur in both strings.
    return all(count == 0 for count in counts)


class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        return is_anagram_optimal(s, t)


def main() -> None:
    cases = [('anagram', 'nagaram', True), ('rat', 'car', False),
             ('a', 'a', True), ('a', 'b', False), ('ab', 'a', False),
             ('aab', 'abb', False), ('aazz', 'zaza', True)]
    for s, t, expected in cases:
        lengthy = is_anagram_lengthy(s, t)
        optimal = is_anagram_optimal(s, t)
        assert lengthy == optimal == expected, (s, t, lengthy, optimal)
        print(f'{s=}, {t=}: lengthy={lengthy}, optimal={optimal}')


if __name__ == '__main__':
    main()
