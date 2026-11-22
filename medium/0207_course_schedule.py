"""207. Course Schedule — Medium.
https://leetcode.com/problems/course-schedule/

Constraints: 1 <= numCourses <= 2000; 0 <= len(prerequisites) <= 5000.
Unique pairs [course, prerequisite] use labels 0..numCourses-1.
"""
from collections import deque


def can_finish_straightforward(n: int, prerequisites: list[list[int]]) -> bool:
    """Repeatedly scan for available courses. O(n(n+E)) time, O(n) space."""
    completed = [False] * n
    remaining = n
    while remaining:
        blocked = [False] * n
        for course, prerequisite in prerequisites:
            if not completed[prerequisite]:
                blocked[course] = True
        progress = False
        for course in range(n):
            if not completed[course] and not blocked[course]:
                completed[course] = True
                remaining -= 1
                progress = True
        # Every remaining course depends on another remaining course: a cycle.
        if not progress:
            return False
    return True


def can_finish_optimal(n: int, prerequisites: list[list[int]]) -> bool:
    """Kahn's topological traversal. O(n+E) time and auxiliary space."""
    dependents = [[] for _ in range(n)]
    indegree = [0] * n
    for course, prerequisite in prerequisites:
        dependents[prerequisite].append(course)
        indegree[course] += 1
    ready = deque(course for course in range(n) if indegree[course] == 0)
    finished = 0
    while ready:
        course = ready.popleft()
        finished += 1
        for dependent in dependents[course]:
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                ready.append(dependent)
    # Cyclic dependencies can never reach zero remaining prerequisites.
    return finished == n


class Solution:
    def canFinish(self, numCourses: int, prerequisites: list[list[int]]) -> bool:
        return can_finish_optimal(numCourses, prerequisites)


def main() -> None:
    from itertools import permutations

    cases = [(2, [[1, 0]], True), (2, [[1, 0], [0, 1]], False),
             (1, [], True), (1, [[0, 0]], False),
             (4, [[1, 0], [3, 2], [2, 3]], False),
             (4, [[1, 0], [2, 0], [3, 1], [3, 2]], True)]
    for n, edges, expected in cases:
        assert can_finish_straightforward(n, edges) == expected
        assert can_finish_optimal(n, edges) == expected
        assert Solution().canFinish(n, edges) == expected

    checked = 0
    for n in range(1, 5):
        possible = [(a, b) for a in range(n) for b in range(n) if a != b]
        positions = []
        for order in permutations(range(n)):
            positions.append({course: i for i, course in enumerate(order)})
        for mask in range(1 << len(possible)):
            edges = [list(pair) for i, pair in enumerate(possible) if mask >> i & 1]
            # Independent oracle: does any complete ordering obey every edge?
            expected = any(all(pos[b] < pos[a] for a, b in edges) for pos in positions)
            assert can_finish_straightforward(n, edges) == expected
            assert can_finish_optimal(n, edges) == expected
            checked += 1
        for course in range(n):
            assert not can_finish_straightforward(n, [[course, course]])
            assert not can_finish_optimal(n, [[course, course]])
    chain = [[i, i - 1] for i in range(1, 2000)]
    dense = [[a, b] for a in range(1, 101) for b in range(a)][:5000]
    for solve in (can_finish_straightforward, can_finish_optimal):
        assert solve(2000, chain)
        assert not solve(2000, chain + [[0, 1999]])
        assert solve(2000, dense)
        assert solve(2000, [])
    print(f"Course Schedule: {checked} exhaustive graphs, self-loops, examples, and bounds passed")


if __name__ == '__main__':
    main()
