"""LeetCode 121: Best Time to Buy and Sell Stock (Easy).

https://leetcode.com/problems/best-time-to-buy-and-sell-stock/
Find the greatest profit from one purchase followed by a later sale, or zero.
Constraints: 1 <= len(prices) <= 100_000; 0 <= prices[i] <= 10_000.
Neither approach changes the input. The quadratic version is for learning;
use the linear version for large inputs and interviews.
"""


def max_profit_lengthy(prices: list[int]) -> int:
    """Check every valid buy/sell pair. Time: O(n²). Extra space: O(1)."""
    best = 0
    for buy in range(len(prices)):
        for sell in range(buy + 1, len(prices)):
            best = max(best, prices[sell] - prices[buy])
    return best


def max_profit_optimal(prices: list[int]) -> int:
    """Track the cheapest earlier purchase. Time: O(n). Extra space: O(1)."""
    cheapest = prices[0]
    best = 0
    for day in range(1, len(prices)):
        # Evaluate the sale before updating the minimum: buy must precede sell.
        best = max(best, prices[day] - cheapest)
        cheapest = min(cheapest, prices[day])
    return best


class Solution:
    """LeetCode-compatible entry point."""

    def maxProfit(self, prices: list[int]) -> int:
        return max_profit_optimal(prices)


def main() -> None:
    cases = [([7, 1, 5, 3, 6, 4], 5), ([7, 6, 4, 3, 1], 0),
             ([5], 0), ([2, 2, 2], 0), ([0, 10_000], 10_000),
             ([10_000, 0], 0), ([3, 1, 4, 0, 2], 3)]
    for prices, expected in cases:
        lengthy = max_profit_lengthy(prices)
        optimal = max_profit_optimal(prices)
        assert lengthy == optimal == expected, (prices, lengthy, optimal)
        print(f"prices={prices}: lengthy={lengthy}, optimal={optimal}")


if __name__ == "__main__":
    main()
