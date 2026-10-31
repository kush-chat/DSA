"""LeetCode 125: Valid Palindrome (Easy).

https://leetcode.com/problems/valid-palindrome/
Compare letters and digits case-insensitively, ignoring other characters.
Constraints: 1 <= len(s) <= 200_000; printable ASCII characters only.
"""


def is_palindrome_lengthy(s: str) -> bool:
    """Build a normalized sequence. Time O(n), extra space O(n)."""
    normalized = []
    for char in s:
        if char.isalnum():
            normalized.append(char.lower())
    for index in range(len(normalized) // 2):
        if normalized[index] != normalized[len(normalized) - 1 - index]:
            return False
    return True


def is_palindrome_optimal(s: str) -> bool:
    """Scan inward without copying the string. Time O(n), extra space O(1)."""
    left, right = 0, len(s) - 1
    while left < right:
        # Skip punctuation independently on each side.
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True


class Solution:
    def isPalindrome(self, s: str) -> bool:
        return is_palindrome_optimal(s)


def main() -> None:
    cases = [('A man, a plan, a canal: Panama', True), ('race a car', False),
             (' ', True), ('.,!', True), ('a', True), ('0P', False),
             ('aA', True), ('1a2a1', True), ('ab', False)]
    for s, expected in cases:
        lengthy = is_palindrome_lengthy(s)
        optimal = is_palindrome_optimal(s)
        assert lengthy == optimal == expected
        assert Solution().isPalindrome(s) == expected
        print(f'{s!r}: lengthy={lengthy}, optimal={optimal}')


if __name__ == '__main__':
    main()
