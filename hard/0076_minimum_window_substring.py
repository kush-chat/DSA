"""76. Minimum Window Substring — Hard.
https://leetcode.com/problems/minimum-window-substring/
Constraints: 1 <= len(s), len(t) <= 100000; uppercase/lowercase English letters.
Multiplicity matters. LeetCode guarantees a unique answer; ties here use the first.
"""
from collections import Counter
from itertools import product


def min_window_straightforward(s: str, t: str) -> str:
    """Extend each possible start: O(len(s)**2 + len(t)) time, O(52) auxiliary space."""
    if len(t) > len(s):
        return ''
    needed = Counter(t)
    best_start, best_length = 0, len(s) + 1
    for left in range(len(s) - len(t) + 1):
        counts = {}
        missing = len(t)
        for right in range(left, len(s)):
            char = s[right]
            if char in needed:
                previous = counts.get(char, 0)
                counts[char] = previous + 1
                if previous < needed[char]:
                    missing -= 1
            if missing == 0:
                length = right - left + 1
                if length < best_length:
                    best_start, best_length = left, length
                # No longer window with this start can improve the result.
                break
        if best_length == len(t):
            break  # No valid answer can be shorter than t.
    if best_length == len(s) + 1:
        return ''
    return s[best_start:best_start + best_length]


def min_window_optimal(s: str, t: str) -> str:
    """Sliding window: O(len(s)+len(t)) time, O(52) space excluding returned slice."""
    needed = Counter(t)
    missing = len(t)
    left = 0
    best_start, best_length = 0, len(s) + 1
    for right, char in enumerate(s):
        if needed[char] > 0:
            missing -= 1
        needed[char] -= 1  # Negative counts represent surplus copies.
        while missing == 0:
            length = right - left + 1
            if length < best_length:
                best_start, best_length = left, length
            outgoing = s[left]
            needed[outgoing] += 1
            if needed[outgoing] > 0:
                missing += 1
            left += 1
    return '' if best_length > len(s) else s[best_start:best_start + best_length]


class Solution:
    def minWindow(self, s: str, t: str) -> str:
        return min_window_optimal(s, t)


def check(s, t, expected):
    assert min_window_straightforward(s, t) == expected, (s, t, expected)
    assert min_window_optimal(s, t) == expected, (s, t, expected)
    assert Solution().minWindow(s, t) == expected


def oracle(s, t):
    # Enumerate by length then start; recompute character counts independently.
    required = Counter(t)
    for length in range(len(t), len(s) + 1):
        for start in range(len(s) - length + 1):
            candidate = s[start:start + length]
            counts = Counter(candidate)
            if all(counts[char] >= count for char, count in required.items()):
                return candidate
    return ''


def main() -> None:
    for s, t, expected in [
        ('ADOBECODEBANC', 'ABC', 'BANC'), ('a', 'a', 'a'), ('a', 'aa', ''),
        ('AAABBC', 'AABC', 'AABBC'), ('aA', 'A', 'A'), ('abc', 'z', ''),
        ('bba', 'ab', 'ba'), ('A' * 100000, 'A' * 100000, 'A' * 100000),
        ('A' * 99999 + 'B', 'B', 'B'),
    ]:
        # The final large case is checked below only with the linear solution.
        if len(s) == 100000 and t == 'B':
            assert min_window_optimal(s, t) == expected
        else:
            check(s, t, expected)
    count = 0
    for size in range(1, 8):
        for chars in product('aA', repeat=size):
            s = ''.join(chars)
            for target_size in range(1, 5):
                for target_chars in product('aA', repeat=target_size):
                    t = ''.join(target_chars)
                    check(s, t, oracle(s, t))
                    count += 1
    print(f'76: examples, bounds, and {count} exhaustive cases passed')


if __name__ == '__main__':
    main()
