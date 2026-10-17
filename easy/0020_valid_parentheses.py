"""LeetCode 20: Valid Parentheses (Easy).

https://leetcode.com/problems/valid-parentheses/
Check whether bracket types and nesting match throughout a string.
Constraints: 1 <= len(s) <= 10_000; characters are drawn from ()[]{}.
The lengthy approach illustrates cancellation; use the stack in interviews.
"""


def is_valid_lengthy(s: str) -> bool:
    """Repeatedly remove adjacent pairs. Time: O(n²). Extra space: O(n)."""
    while s:
        reduced = s.replace("()", "").replace("[]", "").replace("{}", "")
        # Every nonempty valid bracket string has an innermost adjacent pair.
        if reduced == s:
            return False
        s = reduced
    return True


def is_valid_optimal(s: str) -> bool:
    """Match each closer with the latest opener. Time: O(n). Space: O(n)."""
    matching = {')': '(', ']': '[', '}': '{'}
    stack: list[str] = []
    for char in s:
        if char in matching:
            if not stack or stack.pop() != matching[char]:
                return False
        else:
            stack.append(char)
    return not stack


class Solution:
    """LeetCode-compatible entry point."""

    def isValid(self, s: str) -> bool:
        return is_valid_optimal(s)


def main() -> None:
    cases = [("()", True), ("()[]{}", True), ("(]", False),
             ("([])", True), ("([)]", False), ("{[()]}", True),
             ("]", False), ("(", False), (")(", False), ("(()", False)]
    for s, expected in cases:
        lengthy = is_valid_lengthy(s)
        optimal = is_valid_optimal(s)
        assert lengthy == optimal == expected, (s, lengthy, optimal)
        print(f"s={s!r}: lengthy={lengthy}, optimal={optimal}")


if __name__ == "__main__":
    main()
