"""322. Coin Change — Medium.
https://leetcode.com/problems/coin-change/
Constraints: 1..12 denominations, each in [1, 2**31-1]; 0 <= amount <= 10000.
Coins may be reused without limit. Return -1 when the amount is unreachable.
"""
from collections import deque
from itertools import combinations


def coin_change_straightforward(coins: list[int], amount: int) -> int:
    """Explicit denomination/amount table: O(k*A) time and space (A=amount+1)."""
    unreachable = amount + 1
    table = [[unreachable] * (amount + 1) for _ in range(len(coins) + 1)]
    # Zero coins suffice for zero amount, regardless of available denominations.
    for row in table:
        row[0] = 0
    for count in range(1, len(coins) + 1):
        coin = coins[count - 1]
        for subtotal in range(1, amount + 1):
            # Option 1: do not use this denomination.
            best = table[count - 1][subtotal]
            if coin <= subtotal:
                # Stay in this row to allow another copy of the same coin.
                remainder = table[count][subtotal - coin]
                if remainder != unreachable:
                    using_coin = remainder + 1
                    if using_coin < best:
                        best = using_coin
            table[count][subtotal] = best
    answer = table[-1][amount]
    return -1 if answer == unreachable else answer


def coin_change_optimal(coins: list[int], amount: int) -> int:
    """Standard compressed DP: O(k*A) time, O(A) space; A=amount+1."""
    unreachable = amount + 1
    best = [0] + [unreachable] * amount
    for coin in coins:
        # Ascending amounts allow unlimited reuse of this denomination.
        for subtotal in range(coin, amount + 1):
            best[subtotal] = min(best[subtotal], best[subtotal - coin] + 1)
    return -1 if best[amount] == unreachable else best[amount]


class Solution:
    def coinChange(self, coins: list[int], amount: int) -> int:
        return coin_change_optimal(coins, amount)


def check(coins, amount, expected):
    original = coins.copy()
    assert coin_change_straightforward(coins, amount) == expected
    assert coin_change_optimal(coins, amount) == expected
    assert Solution().coinChange(coins, amount) == expected
    assert coins == original


def bfs_oracle(coins, amount):
    """Independent shortest-path search: each edge adds one coin."""
    queue = deque([(0, 0)])
    seen = {0}
    while queue:
        subtotal, count = queue.popleft()
        if subtotal == amount:
            return count
        for coin in coins:
            following = subtotal + coin
            if following <= amount and following not in seen:
                seen.add(following)
                queue.append((following, count + 1))
    return -1


def main() -> None:
    for coins, amount, expected in [
        ([1, 2, 5], 11, 3), ([2], 3, -1), ([1], 0, 0),
        ([1, 3, 4], 6, 2),  # Largest-first greedy would use three coins.
        ([2, 4], 7, -1), ([2**31 - 1], 10000, -1),
        ([1], 10000, 10000), (list(range(1, 13)), 10000, 834),
        ([5, 2, 1], 11, 3), ([2, 2], 4, 2),
    ]:
        check(coins, amount, expected)
    tested = 0
    for size in range(1, 7):
        for denominations in combinations(range(1, 7), size):
            for amount in range(41):
                coins = list(denominations)
                check(coins, amount, bfs_oracle(coins, amount))
                tested += 1
    print(f'322: examples, bounds, and {tested} BFS-oracle cases passed')


if __name__ == '__main__':
    main()
