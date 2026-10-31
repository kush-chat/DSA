"""LeetCode 680: Valid Palindrome II (Easy).

https://leetcode.com/problems/valid-palindrome-ii/
Decide whether deleting at most one character can produce a palindrome.
Constraints: 1 <= len(s) <= 100_000; lowercase English letters only.
The quadratic baseline is educational; use the optimal version for large inputs.
"""


def valid_palindrome_lengthy(s: str) -> bool:
    """Try each deletion explicitly. Time O(n**2), peak extra space O(n)."""
    if s == s[::-1]:
        return True
    for removed in range(len(s)):
        candidate = s[:removed] + s[removed + 1:]
        if candidate == candidate[::-1]:
            return True
    return False


def valid_palindrome_optimal(s: str) -> bool:
    """Check two possible skips at the first mismatch. Time O(n), space O(1)."""
    def is_palindrome_range(left: int, right: int) -> bool:
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True

    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            # Any successful deletion must resolve this mismatched pair.
            # The remaining range must be a palindrome with no further deletions.
            return (is_palindrome_range(left + 1, right)
                    or is_palindrome_range(left, right - 1))
        left += 1
        right -= 1
    return True


class Solution:
    def validPalindrome(self, s: str) -> bool:
        return valid_palindrome_optimal(s)


def main() -> None:
    cases = [('aba', True), ('abca', True), ('abc', False), ('a', True),
             ('ab', True), ('deeee', True), ('eeeed', True),
             ('abcba', True), ('abecbea', False), ('aab', True)]
    for s, expected in cases:
        lengthy = valid_palindrome_lengthy(s)
        optimal = valid_palindrome_optimal(s)
        assert lengthy == optimal == expected
        assert Solution().validPalindrome(s) == expected
        print(f'{s!r}: lengthy={lengthy}, optimal={optimal}')


if __name__ == '__main__':
    main()
