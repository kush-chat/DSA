"""1047. Remove All Adjacent Duplicates In String — Easy.
https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string/
Constraints: 1 <= len(s) <= 100_000; lowercase English letters.
"""


def remove_straightforward(s: str) -> str:
    """Repeatedly scan and remove disjoint equal pairs until stable.
    O(n**2) worst-case time from cascading passes; O(n) peak extra space.
    """
    current = s
    while True:
        remaining: list[str] = []
        removed_pair = False
        index = 0
        while index < len(current):
            if index + 1 < len(current) and current[index] == current[index + 1]:
                removed_pair = True
                index += 2
            else:
                remaining.append(current[index])
                index += 1
        if not removed_pair:
            return current
        current = ''.join(remaining)


def remove_optimal(s: str) -> str:
    """Maintain the fully reduced prefix as a stack. O(n) time, O(n) space.
    Each letter is pushed once or cancels the top; new neighbors are handled
    immediately, including cascades that would require more scanning passes.
    """
    stack: list[str] = []
    for character in s:
        if stack and stack[-1] == character:
            stack.pop()
        else:
            stack.append(character)
    return ''.join(stack)


class Solution:
    def removeDuplicates(self, s: str) -> str:
        return remove_optimal(s)


def main() -> None:
    cases = [('abbaca', 'ca'), ('azxxzy', 'ay'), ('a', 'a'),
             ('aa', ''), ('aaa', 'a'), ('abba', ''), ('abc', 'abc'),
             ('abccba', ''), ('a' * 100_000, ''),
             ('ab' * 50_000, 'ab' * 50_000)]
    for s, expected in cases:
        assert remove_straightforward(s) == expected
        assert remove_optimal(s) == expected
        assert Solution().removeDuplicates(s) == expected
    print('Remove All Adjacent Duplicates In String: all checks passed.')


if __name__ == '__main__':
    main()
