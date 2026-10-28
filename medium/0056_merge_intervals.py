"""LeetCode 56: Merge Intervals (Medium).

https://leetcode.com/problems/merge-intervals/
Merge overlapping closed intervals, including intervals touching at endpoints.
Constraints: 1..10_000 intervals; 0 <= start <= end <= 10_000.
Both solutions return fresh interval lists without mutating the input.
"""


def merge_lengthy(intervals: list[list[int]]) -> list[list[int]]:
    """Find overlap components by graph traversal. Time: O(n²). Space: O(n)."""
    visited = [False] * len(intervals)
    merged = []
    for root in range(len(intervals)):
        if visited[root]:
            continue
        visited[root] = True
        pending = [root]
        start, end = intervals[root]
        while pending:
            index = pending.pop()
            left, right = intervals[index]
            start, end = min(start, left), max(end, right)
            for other, (a, b) in enumerate(intervals):
                if not visited[other] and left <= b and a <= right:
                    visited[other] = True
                    pending.append(other)
        merged.append([start, end])
    return sorted(merged)


def merge_optimal(intervals: list[list[int]]) -> list[list[int]]:
    """Sort by start and sweep. Time: O(n log n). Space: O(n)."""
    merged: list[list[int]] = []
    for start, end in sorted(intervals):
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            # Sorted starts mean only the latest merged interval can overlap.
            merged[-1][1] = max(merged[-1][1], end)
    return merged


class Solution:
    def merge(self, intervals: list[list[int]]) -> list[list[int]]:
        return merge_optimal(intervals)


def main() -> None:
    cases = [([[1, 3], [2, 6], [8, 10], [15, 18]], [[1, 6], [8, 10], [15, 18]]),
             ([[1, 4], [4, 5]], [[1, 5]]), ([[4, 7], [1, 4]], [[1, 7]]),
             ([[0, 0]], [[0, 0]]), ([[1, 5], [2, 3], [1, 5]], [[1, 5]]),
             ([[1, 2], [5, 6], [2, 5]], [[1, 6]])]
    for intervals, expected in cases:
        lengthy = merge_lengthy(intervals)
        optimal = merge_optimal(intervals)
        assert lengthy == optimal == expected
        print(f'{intervals=}: lengthy={lengthy}, optimal={optimal}')


if __name__ == '__main__':
    main()
