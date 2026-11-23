"""455. Assign Cookies — Easy.
https://leetcode.com/problems/assign-cookies/

Constraints: 1 <= len(g) <= 30000; 0 <= len(s) <= 30000;
all greed factors and cookie sizes are in [1, 2**31 - 1].
"""


def assign_straightforward(g: list[int], s: list[int]) -> int:
    """Scan for the smallest usable cookie. O(n log n + nm) time, O(n+m) space."""
    children = sorted(g)
    used = [False] * len(s)
    satisfied = 0
    for greed in children:
        chosen = -1
        for index, size in enumerate(s):
            if used[index] or size < greed:
                continue
            if chosen == -1 or size < s[chosen]:
                chosen = index
        if chosen == -1:
            # Later children need at least as much, so none can be satisfied.
            break
        used[chosen] = True
        satisfied += 1
    return satisfied


def assign_optimal(g: list[int], s: list[int]) -> int:
    """Sorted two pointers: O(n log n + m log m) time, O(n+m) space."""
    children = sorted(g)
    cookies = sorted(s)
    child = 0
    for size in cookies:
        if child == len(children):
            break
        if size >= children[child]:
            # The smallest sufficient cookie leaves larger ones for harder needs.
            child += 1
        # A smaller cookie cannot satisfy this child or any later child.
    return child


class Solution:
    def findContentChildren(self, g: list[int], s: list[int]) -> int:
        return assign_optimal(g, s)


def main() -> None:
    from functools import lru_cache
    from itertools import product

    def oracle(g: tuple[int, ...], s: tuple[int, ...]) -> int:
        @lru_cache(None)
        def match(child: int, used: int) -> int:
            if child == len(g):
                return 0
            best = match(child + 1, used)
            for i, size in enumerate(s):
                if not (used >> i & 1) and size >= g[child]:
                    best = max(best, 1 + match(child + 1, used | (1 << i)))
            return best
        return match(0, 0)

    cases = [([1, 2, 3], [1, 1], 1), ([1, 2], [1, 2, 3], 2),
             ([1], [], 0), ([2, 2], [2], 1), ([3], [1, 2], 0),
             ([2**31 - 1], [2**31 - 1], 1)]
    for g, s, expected in cases:
        for solve in (assign_straightforward, assign_optimal):
            assert solve(g, s) == expected
        assert Solution().findContentChildren(g, s) == expected
    checked = 0
    for n in range(1, 5):
        for m in range(5):
            for g in product((1, 2), repeat=n):
                for s in product((1, 2), repeat=m):
                    expected = oracle(g, s)
                    assert assign_straightforward(list(g), list(s)) == expected
                    assert assign_optimal(list(g), list(s)) == expected
                    checked += 1
    for solve in (assign_straightforward, assign_optimal):
        assert solve([2**31 - 1] * 30000, [1] * 30000) == 0
        assert solve([1] * 30000, []) == 0
    assert assign_optimal([1] * 30000, [1] * 30000) == 30000
    print(f"Assign Cookies: {checked} exhaustive cases, examples, and bounds passed")


if __name__ == '__main__':
    main()
