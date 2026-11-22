"""997. Find the Town Judge — Easy.
https://leetcode.com/problems/find-the-town-judge/

Constraints: 1 <= n <= 1000; 0 <= len(trust) <= 10**4.
Pairs are unique, labels are in 1..n, and nobody trusts themselves.
"""


def find_judge_straightforward(n: int, trust: list[list[int]]) -> int:
    """Check each candidate by scanning every edge. O(n(E+1)) time, O(1) space."""
    for candidate in range(1, n + 1):
        trusts_someone = False
        incoming = 0
        for source, target in trust:
            if source == candidate:
                trusts_someone = True
            if target == candidate:
                incoming += 1
        # Unique edges make the incoming count equal to distinct supporters.
        if not trusts_someone and incoming == n - 1:
            return candidate
    return -1


def find_judge_optimal(n: int, trust: list[list[int]]) -> int:
    """Net indegree scores: O(n+E) time, O(n) auxiliary space."""
    score = [0] * (n + 1)
    for source, target in trust:
        score[source] -= 1
        score[target] += 1
    for person in range(1, n + 1):
        # Indegree is at most n-1. Reaching that score forces outdegree zero.
        if score[person] == n - 1:
            return person
    return -1


class Solution:
    def findJudge(self, n: int, trust: list[list[int]]) -> int:
        return find_judge_optimal(n, trust)


def main() -> None:
    cases = [(2, [[1, 2]], 2), (3, [[1, 3], [2, 3]], 3),
             (3, [[1, 3], [2, 3], [3, 1]], -1), (1, [], 1), (2, [], -1)]
    for n, edges, expected in cases:
        assert find_judge_straightforward(n, edges) == expected
        assert find_judge_optimal(n, edges) == expected
        assert Solution().findJudge(n, edges) == expected

    checked = 0
    for n in range(1, 5):
        possible = [(a, b) for a in range(1, n + 1)
                    for b in range(1, n + 1) if a != b]
        for mask in range(1 << len(possible)):
            edges = [list(pair) for i, pair in enumerate(possible) if mask >> i & 1]
            relationships = set(map(tuple, edges))
            # Independent oracle checks the two defining properties directly.
            candidates = [p for p in range(1, n + 1)
                          if all((p, q) not in relationships and (q, p) in relationships
                                 for q in range(1, n + 1) if q != p)]
            expected = candidates[0] if candidates else -1
            assert find_judge_straightforward(n, edges) == expected
            assert find_judge_optimal(n, edges) == expected
            checked += 1
    edges = [[p, 1000] for p in range(1, 1000)]
    for a in range(1, 1000):
        for b in range(1, 1000):
            if a != b and len(edges) < 10000:
                edges.append([a, b])
        if len(edges) == 10000:
            break
    for solve in (find_judge_straightforward, find_judge_optimal):
        assert solve(1000, edges) == 1000
        assert solve(1000, []) == -1
    print(f"Town Judge: {checked} exhaustive graphs, examples, and bounds passed")


if __name__ == '__main__':
    main()
