"""202. Happy Number — Easy.
https://leetcode.com/problems/happy-number/
Constraint: 1 <= n <= 2**31 - 1.
"""


def digit_square_sum(number: int) -> int:
    total = 0
    while number:
        number, digit = divmod(number, 10)
        total += digit * digit
    return total


def happy_straightforward(n: int) -> bool:
    """Remember each visited state until reaching 1 or repeating a state.
    For k visited states with at most d digits: O(k*d) time, O(k) space.
    Under the stated bound, the first step is <= 810, so k is bounded.
    """
    visited: set[int] = set()
    current = n
    while current != 1:
        if current in visited:
            return False
        visited.add(current)
        next_number = 0
        remaining_digits = current
        while remaining_digits > 0:
            last_digit = remaining_digits % 10
            next_number += last_digit * last_digit
            remaining_digits //= 10
        current = next_number
    return True


def happy_optimal(n: int) -> bool:
    """Floyd cycle detection: O(k*d) time, O(1) extra space.
    A happy trajectory ends in the self-loop at 1; others enter another cycle.
    """
    slow = n
    fast = digit_square_sum(n)
    while fast != 1 and slow != fast:
        slow = digit_square_sum(slow)
        fast = digit_square_sum(digit_square_sum(fast))
    return fast == 1


class Solution:
    def isHappy(self, n: int) -> bool:
        return happy_optimal(n)


def main() -> None:
    cases = [(19, True), (2, False), (1, True), (7, True), (10, True),
             (4, False), (100, True), (1_000_000_000, True),
             (2**31 - 1, False)]
    for n, expected in cases:
        assert happy_straightforward(n) == expected
        assert happy_optimal(n) == expected
        assert Solution().isHappy(n) == expected
    print('Happy Number: all checks passed.')


if __name__ == '__main__':
    main()
