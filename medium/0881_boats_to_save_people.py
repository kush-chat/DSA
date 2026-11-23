"""881. Boats to Save People — Medium.
https://leetcode.com/problems/boats-to-save-people/

Constraints: 1 <= len(people) <= 50000; 1 <= weight <= limit <= 30000.
Each boat holds at most two people and total weight at most limit.
"""


def boats_straightforward(people: list[int], limit: int) -> int:
    """Sort and remove passengers explicitly. O(n**2) time, O(n) space."""
    waiting = sorted(people)
    boats = 0
    while waiting:
        heaviest = waiting.pop()
        boats += 1
        if not waiting:
            break
        lightest = waiting[0]
        if lightest + heaviest <= limit:
            # Removing index zero shifts the remaining list: the costly step.
            waiting.pop(0)
        # If even the lightest cannot join, the heaviest must travel alone.
    return boats


def boats_optimal(people: list[int], limit: int) -> int:
    """Count bounded weights, then pair extremes. O(n+limit) time, O(limit) space."""
    counts = [0] * (limit + 1)
    for weight in people:
        counts[weight] += 1
    low, high = 1, limit
    remaining = len(people)
    boats = 0
    while remaining:
        while counts[high] == 0:
            high -= 1
        heaviest = high
        counts[high] -= 1
        remaining -= 1
        boats += 1
        if not remaining:
            break
        while counts[low] == 0:
            low += 1
        if low + heaviest <= limit:
            # Pairing with the lightest never worsens an optimal arrangement:
            # swap partners if necessary; both replacement pairs still fit.
            counts[low] -= 1
            remaining -= 1
    return boats


class Solution:
    def numRescueBoats(self, people: list[int], limit: int) -> int:
        return boats_optimal(people, limit)


def main() -> None:
    from functools import lru_cache
    from itertools import product

    def oracle(weights: tuple[int, ...], limit: int) -> int:
        @lru_cache(None)
        def arrange(mask: int) -> int:
            if not mask:
                return 0
            first = (mask & -mask).bit_length() - 1
            rest = mask ^ (1 << first)
            best = 1 + arrange(rest)
            for partner in range(first + 1, len(weights)):
                if rest >> partner & 1 and weights[first] + weights[partner] <= limit:
                    best = min(best, 1 + arrange(rest ^ (1 << partner)))
            return best
        return arrange((1 << len(weights)) - 1)

    cases = [([1, 2], 3, 1), ([3, 2, 2, 1], 3, 3), ([3, 5, 3, 4], 5, 4),
             ([1], 1, 1), ([2, 2, 2], 4, 2), ([1, 1, 1, 1], 2, 2)]
    for people, limit, expected in cases:
        for solve in (boats_straightforward, boats_optimal):
            original = people.copy()
            assert solve(people, limit) == expected
            assert people == original
        assert Solution().numRescueBoats(people, limit) == expected
    checked = 0
    for n in range(1, 8):
        for values in product((1, 2, 3), repeat=n):
            for limit in range(max(values), 7):
                expected = oracle(values, limit)
                assert boats_straightforward(list(values), limit) == expected
                assert boats_optimal(list(values), limit) == expected
                checked += 1
    for solve in (boats_straightforward, boats_optimal):
        assert solve([30000] * 50000, 30000) == 50000
        assert solve([15000] * 50000, 30000) == 25000
        assert solve([1] * 49999, 30000) == 25000
    print(f"Boats: {checked} exhaustive cases, examples, and bounds passed")


if __name__ == '__main__':
    main()
