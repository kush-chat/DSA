"""844. Backspace String Compare — Easy.
https://leetcode.com/problems/backspace-string-compare/
Constraints: string lengths 1..200; lowercase English letters and '#'.
"""


def compare_straightforward(s: str, t: str) -> bool:
    """Simulate both editors. O(len(s)+len(t)) time and extra space."""
    def type_text(text: str) -> list[str]:
        editor: list[str] = []
        for character in text:
            if character == '#':
                if editor:
                    editor.pop()
            else:
                editor.append(character)
        return editor

    first_editor = type_text(s)
    second_editor = type_text(t)
    if len(first_editor) != len(second_editor):
        return False
    for index in range(len(first_editor)):
        if first_editor[index] != second_editor[index]:
            return False
    return True


def compare_optimal(s: str, t: str) -> bool:
    """Scan surviving characters backwards: O(len(s)+len(t)) time, O(1) space."""
    def previous_visible(text: str, index: int) -> int:
        pending = 0
        while index >= 0:
            if text[index] == '#':
                pending += 1
            elif pending:
                pending -= 1
            else:
                return index
            index -= 1
        return -1

    i, j = len(s) - 1, len(t) - 1
    while i >= 0 or j >= 0:
        i = previous_visible(s, i)
        j = previous_visible(t, j)
        if i < 0 or j < 0:
            return i == j  # Both editors must run out together.
        if s[i] != t[j]:
            return False
        i -= 1
        j -= 1
    return True


class Solution:
    def backspaceCompare(self, s: str, t: str) -> bool:
        return compare_optimal(s, t)


def main() -> None:
    cases = [('ab#c', 'ad#c', True), ('ab##', 'c#d#', True),
             ('a#c', 'b', False), ('###a', 'a', True), ('#', 'a#', True),
             ('a', 'b', False), ('a', 'a#', False),
             ('a' * 100 + '#' * 100, '#' * 200, True),
             ('a' * 200, 'a' * 199 + 'b', False)]
    for s, t, expected in cases:
        assert compare_straightforward(s, t) == expected
        assert compare_optimal(s, t) == expected
        assert Solution().backspaceCompare(s, t) == expected
    print('Backspace String Compare: all checks passed.')


if __name__ == '__main__':
    main()
