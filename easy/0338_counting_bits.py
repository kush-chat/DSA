"""LeetCode 338: Counting Bits (Easy).

https://leetcode.com/problems/counting-bits/
Return the number of set bits for every integer from zero through n.
Constraint: 0 <= n <= 100_000. Neither solution uses a built-in bit counter.
"""


def count_bits_lengthy(n: int) -> list[int]:
    """Inspect each binary digit. Time: O(n log(n+1)). Space: O(n) for output."""
    answer = []
    for number in range(n + 1):
        count = 0
        remaining = number
        while remaining:
            count += remaining & 1
            remaining >>= 1
        answer.append(count)
    return answer


def count_bits_optimal(n: int) -> list[int]:
    """Reuse the answer for half the number. Time: O(n). Space: O(n) for output."""
    answer = [0] * (n + 1)
    for number in range(1, n + 1):
        # Shifting removes the last bit; add that bit back to the smaller answer.
        answer[number] = answer[number >> 1] + (number & 1)
    return answer


class Solution:
    def countBits(self, n: int) -> list[int]:
        return count_bits_optimal(n)


def main() -> None:
    cases = [(0, [0]), (1, [0, 1]), (2, [0, 1, 1]),
             (5, [0, 1, 1, 2, 1, 2]), (8, [0, 1, 1, 2, 1, 2, 2, 3, 1])]
    for n, expected in cases:
        lengthy = count_bits_lengthy(n)
        optimal = count_bits_optimal(n)
        assert lengthy == optimal == expected
        print(f'{n=}: lengthy={lengthy}, optimal={optimal}')


if __name__ == '__main__':
    main()
