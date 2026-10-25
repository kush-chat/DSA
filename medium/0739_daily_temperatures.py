"""LeetCode 739: Daily Temperatures (Medium).

https://leetcode.com/problems/daily-temperatures/
Return the wait until a strictly warmer day, or zero if there is none.
Constraints: 1..100_000 temperatures; values 30..100.
Neither solution mutates input. The quadratic baseline is for learning;
use the linear stack solution for large inputs and interviews.
"""


def daily_temperatures_lengthy(temperatures: list[int]) -> list[int]:
    """Search future days for each day. Time: O(n²). Space: O(1) excluding output."""
    answer = [0] * len(temperatures)
    for today in range(len(temperatures)):
        for future in range(today + 1, len(temperatures)):
            if temperatures[future] > temperatures[today]:
                answer[today] = future - today
                break
    return answer


def daily_temperatures_optimal(temperatures: list[int]) -> list[int]:
    """Maintain unresolved days in a monotonic stack. Time: O(n). Space: O(n)."""
    answer = [0] * len(temperatures)
    stack: list[int] = []
    for today, temperature in enumerate(temperatures):
        # Equal temperatures stay unresolved: the next day must be warmer.
        while stack and temperature > temperatures[stack[-1]]:
            previous = stack.pop()
            answer[previous] = today - previous
        stack.append(today)
    # Each index is pushed and popped at most once; unresolved days remain zero.
    return answer


class Solution:
    def dailyTemperatures(self, temperatures: list[int]) -> list[int]:
        return daily_temperatures_optimal(temperatures)


def main() -> None:
    cases = [([73, 74, 75, 71, 69, 72, 76, 73], [1, 1, 4, 2, 1, 1, 0, 0]),
             ([30, 40, 50, 60], [1, 1, 1, 0]), ([30, 60, 90], [1, 1, 0]),
             ([100], [0]), ([70, 70, 70], [0, 0, 0]),
             ([90, 80, 70], [0, 0, 0]), ([70, 70, 71], [2, 1, 0]),
             ([30, 100, 30, 100], [1, 0, 1, 0])]
    for temperatures, expected in cases:
        lengthy = daily_temperatures_lengthy(temperatures)
        optimal = daily_temperatures_optimal(temperatures)
        assert lengthy == optimal == expected, (temperatures, lengthy, optimal)
        print(f'{temperatures=}: lengthy={lengthy}, optimal={optimal}')


if __name__ == '__main__':
    main()
