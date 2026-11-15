"""746. Min Cost Climbing Stairs — Easy.
https://leetcode.com/problems/min-cost-climbing-stairs/
Constraints: 2 <= len(cost) <= 1000; 0 <= cost[i] <= 999.
Start on step 0 or 1; pay a step's cost when leaving it by one or two steps.
"""
from itertools import product


def min_cost_straightforward(cost: list[int]) -> int:
    """Store and relax all positions: O(n) time and O(n) extra space."""
    top = len(cost)
    minimum = [float('inf')] * (top + 1)
    minimum[0] = 0
    minimum[1] = 0
    for position in range(top):
        # Reaching a step is free; its cost is charged on departure.
        departure_cost = minimum[position] + cost[position]
        one_step = position + 1
        if departure_cost < minimum[one_step]:
            minimum[one_step] = departure_cost
        two_steps = position + 2
        if two_steps <= top:
            if departure_cost < minimum[two_steps]:
                minimum[two_steps] = departure_cost
    return int(minimum[top])


def min_cost_optimal(cost: list[int]) -> int:
    """Keep only the previous two states: O(n) time, O(1) extra space."""
    two_back = one_back = 0
    for position in range(2, len(cost) + 1):
        current = min(one_back + cost[position - 1],
                      two_back + cost[position - 2])
        two_back, one_back = one_back, current
    return one_back


class Solution:
    def minCostClimbingStairs(self, cost: list[int]) -> int:
        return min_cost_optimal(cost)


def check(cost, expected):
    original = cost.copy()
    assert min_cost_straightforward(cost) == expected
    assert min_cost_optimal(cost) == expected
    assert Solution().minCostClimbingStairs(cost) == expected
    assert cost == original


def path_oracle(cost):
    """Enumerate all legal paths for small inputs, without memoization."""
    best = float('inf')
    pending = [(0, 0), (1, 0)]
    while pending:
        position, paid = pending.pop()
        if position >= len(cost):
            best = min(best, paid)
            continue
        paid += cost[position]
        pending.append((position + 1, paid))
        pending.append((position + 2, paid))
    return best


def main() -> None:
    for cost, expected in [
        ([10, 15, 20], 15), ([1, 100, 1, 1, 1, 100, 1, 1, 100, 1], 6),
        ([0, 0], 0), ([999, 0], 0), ([0, 999], 0), ([999, 999], 999),
        ([999] * 1000, 499500), ([0] * 1000, 0), ([999, 0] * 500, 0),
    ]:
        check(cost, expected)
    tested = 0
    for size in range(2, 9):
        for values in product((0, 1, 3), repeat=size):
            cost = list(values)
            check(cost, path_oracle(cost))
            tested += 1
    print(f'746: examples, bounds, and {tested} exhaustive path-oracle cases passed')


if __name__ == '__main__':
    main()
