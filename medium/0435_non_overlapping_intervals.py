"""LeetCode 435: Non-overlapping Intervals (Medium).

https://leetcode.com/problems/non-overlapping-intervals/
Remove the fewest intervals so remaining intervals do not overlap.
Touching endpoints are allowed, unlike LeetCode 56's merging convention.
Constraints: 1..100_000 intervals; -50_000 <= start < end <= 50_000.
Neither approach mutates input. Use the greedy solution for large inputs.
"""


def erase_overlap_lengthy(intervals: list[list[int]]) -> int:
    """DP for the longest compatible chain. Time: O(n²). Space: O(n)."""
    ordered = sorted(intervals)
    best = [1] * len(ordered)
    for current in range(len(ordered)):
        for previous in range(current):
            if ordered[previous][1] <= ordered[current][0]:
                best[current] = max(best[current], best[previous] + 1)
    return len(ordered) - max(best)


def erase_overlap_optimal(intervals: list[list[int]]) -> int:
    """Keep intervals by earliest finish. Time: O(n log n). Space: O(n) for sorting."""
    ordered = sorted(intervals, key=lambda interval: interval[1])
    kept = 1
    previous_end = ordered[0][1]
    for index in range(1, len(ordered)):
        start, end = ordered[index]
        if start >= previous_end:
            # The earliest finish leaves at least as much room as any alternative.
            kept += 1
            previous_end = end
    return len(ordered) - kept


class Solution:
    def eraseOverlapIntervals(self, intervals: list[list[int]]) -> int:
        return erase_overlap_optimal(intervals)


def main() -> None:
    cases = [([[1, 2], [2, 3], [3, 4], [1, 3]], 1),
             ([[1, 2], [1, 2], [1, 2]], 2), ([[1, 2], [2, 3]], 0),
             ([[-50_000, 50_000]], 0), ([[1, 10], [2, 3], [3, 4]], 1),
             ([[-3, -1], [-2, 0], [0, 1]], 1)]
    for intervals, expected in cases:
        lengthy = erase_overlap_lengthy(intervals)
        optimal = erase_overlap_optimal(intervals)
        assert lengthy == optimal == expected
        print(f'{intervals=}: lengthy={lengthy}, optimal={optimal}')


if __name__ == '__main__':
    main()
