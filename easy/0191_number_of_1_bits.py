"""191. Number of 1 Bits — Easy.
https://leetcode.com/problems/number-of-1-bits/
Constraints: 1 <= n <= 2**31 - 1.
"""


def hamming_weight_straightforward(n: int) -> int:
    """Inspect each binary digit arithmetically. O(b) time, O(1) space.

    b is the bit length; bounded by 31 for this problem.
    """
    remaining = n
    count = 0
    while remaining > 0:
        quotient = remaining // 2
        remainder = remaining - quotient * 2
        if remainder == 1:
            count += 1
        remaining = quotient
    return count


def hamming_weight_optimal(n: int) -> int:
    """Clear one set bit per iteration. O(p) time, O(1) space.

    p is the number of set bits; at most 31, hence O(1) for fixed-width input.
    """
    count = 0
    while n:
        # Subtracting one flips the lowest 1 and the zeros below it.
        # AND keeps all higher bits and removes precisely that lowest 1.
        n &= n - 1
        count += 1
    return count


class Solution:
    def hammingWeight(self, n: int) -> int:
        return hamming_weight_optimal(n)


def main() -> None:
    from random import Random

    solvers = (hamming_weight_straightforward, hamming_weight_optimal,
               Solution().hammingWeight)
    cases = [(11, 3), (128, 1), (2147483645, 30), (1, 1), (2**31 - 1, 31)]
    for n, expected in cases:
        for solve in solvers:
            assert solve(n) == expected
    # Independent oracle uses the binary string, not either arithmetic method.
    for n in range(1, 65536):
        expected = bin(n).count('1')
        for solve in solvers:
            assert solve(n) == expected
    for bit in range(31):
        for solve in solvers:
            assert solve(1 << bit) == 1
            assert solve((1 << (bit + 1)) - 1) == bit + 1
    rng = Random(191)
    for _ in range(2000):
        n = rng.randint(1, 2**31 - 1)
        for solve in solvers:
            assert solve(n) == bin(n).count('1')
    print('Number of 1 Bits: 65535 exhaustive values, 2000 random values, and bounds passed')


if __name__ == '__main__':
    main()
