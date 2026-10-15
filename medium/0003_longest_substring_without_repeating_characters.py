"""LeetCode 3: Longest Substring Without Repeating Characters (Medium).

https://leetcode.com/problems/longest-substring-without-repeating-characters/
Return the length of the longest contiguous substring with distinct characters.
"""


def longest_substring_lengthy(s: str) -> int:
    """Expand from every start. Time: O(n²). Space: O(min(n, alphabet size))."""
    longest = 0
    for start in range(len(s)):
        seen: set[str] = set()
        for end in range(start, len(s)):
            if s[end] in seen:
                break
            seen.add(s[end])
            longest = max(longest, end - start + 1)
    return longest


def longest_substring_optimal(s: str) -> int:
    """Sliding window. Expected time: O(n). Space: O(min(n, alphabet size))."""
    last_seen: dict[str, int] = {}
    left = 0
    longest = 0
    for right, char in enumerate(s):
        if char in last_seen:
            # Never move left backwards for a repeat outside the current window.
            left = max(left, last_seen[char] + 1)
        last_seen[char] = right
        longest = max(longest, right - left + 1)
    return longest


class Solution:
    """LeetCode-compatible entry point using the interview solution."""

    def lengthOfLongestSubstring(self, s: str) -> int:
        return longest_substring_optimal(s)


def main() -> None:
    cases = [("abcabcbb", 3), ("bbbbb", 1), ("pwwkew", 3), ("", 0),
             ("a", 1), ("abba", 2), ("dvdf", 3), (" ", 1), ("a b!a", 4)]
    for s, expected in cases:
        lengthy = longest_substring_lengthy(s)
        optimal = longest_substring_optimal(s)
        assert lengthy == optimal == expected, (s, lengthy, optimal, expected)
        print(f"s={s!r}: lengthy={lengthy}, optimal={optimal}")


if __name__ == "__main__":
    main()
