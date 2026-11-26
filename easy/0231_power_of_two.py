"""231. Power of Two — Easy.
https://leetcode.com/problems/power-of-two/
Constraints: -2**31 <= n <= 2**31 - 1.
"""


def is_power_straightforward(n: int) -> bool:
    """Repeated exact division. O(log n) time for n > 0, O(1) space."""
    if n <= 0:
        return False
    remaining = n
    while remaining > 1:
        remainder = remaining % 2
        if remainder != 0:
            # An odd factor greater than one cannot be removed by halving.
            return False
        remaining = remaining // 2
    # One is 2**0, including when it was the original input.
    return True


def is_power_optimal(n: int) -> bool:
    """Test for exactly one set bit. O(1) time and space for 32-bit inputs."""
    # Zero also satisfies the bit expression, so positivity is essential.
    # n & (n-1) removes the lowest set bit: zero remains iff it was the only one.
    return n > 0 and (n & (n - 1)) == 0


class Solution:
    def isPowerOfTwo(self, n: int) -> bool:
        return is_power_optimal(n)


def main() -> None:
    from random import Random

    solvers = (is_power_straightforward, is_power_optimal, Solution().isPowerOfTwo)
    cases = [(1, True), (16, True), (3, False), (0, False), (-16, False),
             (-2**31, False), (2**31 - 1, False), (2**30, True)]
    for n, expected in cases:
        for solve in solvers:
            assert solve(n) is expected
    # Build the oracle by multiplication, independently of division/bit tests.
    powers = set()
    value = 1
    while value <= 2**31 - 1:
        powers.add(value)
        value *= 2
    for n in range(-65536, 65537):
        for solve in solvers:
            assert solve(n) is (n in powers)
    for value in powers:
        for n in (value - 1, value, value + 1, -value):
            for solve in solvers:
                assert solve(n) is (n in powers)
    rng = Random(231)
    for _ in range(2000):
        n = rng.randint(-2**31, 2**31 - 1)
        for solve in solvers:
            assert solve(n) is (n in powers)
    print('Power of Two: 131073 exhaustive values, 2000 random values, and bounds passed')


if __name__ == '__main__':
    main()
