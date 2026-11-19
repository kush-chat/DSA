"""567. Permutation in String — Medium.
https://leetcode.com/problems/permutation-in-string/
Constraints: 1 <= len(s1), len(s2) <= 10000; lowercase English letters only.
"""
from itertools import permutations, product


def includes_straightforward(s1: str, s2: str) -> bool:
    """Recount each window: O(m + (n-m+1)*m) time if m<=n, O(26) space."""
    width = len(s1)
    if width > len(s2):
        return False
    required = [0] * 26
    for char in s1:
        required[ord(char) - ord('a')] += 1
    for start in range(len(s2) - width + 1):
        counts = [0] * 26
        for index in range(start, start + width):
            char = s2[index]
            counts[ord(char) - ord('a')] += 1
        matches = True
        for letter in range(26):
            if counts[letter] != required[letter]:
                matches = False
                break
        if matches:
            return True
    return False


def includes_optimal(s1: str, s2: str) -> bool:
    """Maintain fixed-window frequencies: O(m+n) time, O(26) extra space."""
    width = len(s1)
    if width > len(s2):
        return False
    required, counts = [0] * 26, [0] * 26
    for char in s1:
        required[ord(char) - ord('a')] += 1
    for right, char in enumerate(s2):
        counts[ord(char) - ord('a')] += 1
        if right >= width:
            counts[ord(s2[right - width]) - ord('a')] -= 1
        # Equality costs at most 26 comparisons, independent of string length.
        if right >= width - 1 and counts == required:
            return True
    return False


class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        return includes_optimal(s1, s2)


def check(s1, s2, expected):
    assert includes_straightforward(s1, s2) == expected, (s1, s2)
    assert includes_optimal(s1, s2) == expected, (s1, s2)
    assert Solution().checkInclusion(s1, s2) == expected


def main() -> None:
    for s1, s2, expected in [
        ('ab', 'eidbaooo', True), ('ab', 'eidboaoo', False),
        ('aab', 'ab', False), ('aab', 'xxaba', True),
        ('aab', 'abb', False), ('z', 'a', False), ('a', 'a', True),
        ('a' * 10000, 'a' * 10000, True), ('z', 'a' * 9999 + 'z', True),
        ('z', 'a' * 10000, False),
    ]:
        check(s1, s2, expected)
    count = 0
    for size1 in range(1, 5):
        for chars1 in product('ab', repeat=size1):
            s1 = ''.join(chars1)
            arrangements = {''.join(p) for p in permutations(s1)}
            for size2 in range(1, 8):
                for chars2 in product('ab', repeat=size2):
                    s2 = ''.join(chars2)
                    check(s1, s2, any(p in s2 for p in arrangements))
                    count += 1
    print(f'567: examples, bounds, and {count} permutation-oracle cases passed')


if __name__ == '__main__':
    main()
