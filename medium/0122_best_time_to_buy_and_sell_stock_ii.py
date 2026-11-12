"""122. Best Time to Buy and Sell Stock II — Medium.
https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/
Constraints: 1 <= len(prices) <= 30_000; prices are in [0, 10_000].
Unlimited transactions are allowed, holding at most one share at a time.
"""


def profit_straightforward(prices: list[int]) -> int:
    """Store each day's best cash and holding states: O(n) time, O(n) space.
    Holding includes the purchase cost; cash represents realized profit.
    """
    n = len(prices)
    cash = [0] * n
    holding = [0] * n
    holding[0] = -prices[0]
    for day in range(1, n):
        keep_cash = cash[day - 1]
        sell_today = holding[day - 1] + prices[day]
        cash[day] = max(keep_cash, sell_today)
        keep_share = holding[day - 1]
        buy_today = cash[day - 1] - prices[day]
        holding[day] = max(keep_share, buy_today)
    # Same-day sell/buy at the same price adds no profit, so these transitions
    # suffice even though the problem permits multiple actions on one day.
    return cash[-1]


def profit_optimal(prices: list[int]) -> int:
    """Collect every positive daily rise: O(n) time, O(1) extra space.
    A rising run's daily gains telescope to its buy-low/sell-high profit.
    Avoiding negative daily changes is feasible with unlimited transactions.
    """
    profit = 0
    for day in range(1, len(prices)):
        gain = prices[day] - prices[day - 1]
        if gain > 0:
            profit += gain
    return profit


class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        return profit_optimal(prices)


def main() -> None:
    cases = [([7, 1, 5, 3, 6, 4], 7), ([1, 2, 3, 4, 5], 4),
             ([7, 6, 4, 3, 1], 0), ([0], 0), ([5, 5, 5], 0),
             ([0, 10_000, 0, 10_000], 20_000),
             ([0, 10_000] * 15_000, 150_000_000)]
    for prices, expected in cases:
        original = prices.copy()
        assert profit_straightforward(prices) == expected
        assert profit_optimal(prices) == expected
        assert Solution().maxProfit(prices) == expected
        assert prices == original
    print('Best Time to Buy and Sell Stock II: all checks passed.')


if __name__ == '__main__':
    main()
