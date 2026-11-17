"""74. Search a 2D Matrix — Medium.
https://leetcode.com/problems/search-a-2d-matrix/
Constraints: 1 <= rows, cols <= 100; values and target in [-10000, 10000].
Rows are nondecreasing; each row starts above the previous row's last value.
Solution uses the required O(log(rows*cols)) search without flattening a copy.
"""
from itertools import combinations_with_replacement


def search_straightforward(matrix: list[list[int]], target: int) -> bool:
    """Teaching baseline: scan row ranges then one row, O(rows+cols) time, O(1) space."""
    row_count = len(matrix)
    col_count = len(matrix[0])
    row = 0
    while row < row_count:
        if target < matrix[row][0]:
            # Later rows start even higher, so there can be no match.
            return False
        if target > matrix[row][col_count - 1]:
            row += 1
            continue
        col = 0
        while col < col_count:
            value = matrix[row][col]
            if value == target:
                return True
            if value > target:
                return False
            col += 1
        # The only row whose value range could contain the target has failed.
        return False
    return False


def search_optimal(matrix: list[list[int]], target: int) -> bool:
    """Virtual flattened binary search: O(log(rows*cols+1)) time, O(1) space."""
    rows, cols = len(matrix), len(matrix[0])
    left, right = 0, rows * cols
    while left < right:
        middle = (left + right) // 2
        row, col = divmod(middle, cols)
        value = matrix[row][col]
        if value == target:
            return True
        if value < target:
            left = middle + 1
        else:
            right = middle
    return False


class Solution:
    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        return search_optimal(matrix, target)


def check(matrix, target, expected):
    original = [row[:] for row in matrix]
    assert search_straightforward(matrix, target) == expected
    assert search_optimal(matrix, target) == expected
    assert Solution().searchMatrix(matrix, target) == expected
    assert matrix == original


def main() -> None:
    example = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
    check(example, 3, True)
    check(example, 13, False)
    for matrix, target, expected in [
        ([[0]], 0, True), ([[0]], -1, False),
        ([[-10000, -10000, 0, 10000]], 10000, True),
        ([[-10000], [0], [10000]], -10000, True),
        ([[1, 1, 2], [4, 4, 6]], 3, False),
        ([[1, 1, 2], [4, 4, 6]], 4, True),
    ]:
        check(matrix, target, expected)
    large = [[-10000 + 2 * (r * 100 + c) for c in range(100)] for r in range(100)]
    for target in (-10000, -9999, 0, 9998, 9999, 10000):
        check(large, target, target % 2 == 0 and -10000 <= target <= 9998)
    count = 0
    for rows, cols in ((1, 1), (1, 6), (6, 1), (2, 3), (3, 2)):
        for values in combinations_with_replacement(range(-2, 4), rows * cols):
            # Duplicates within a row are legal, but not across row boundaries.
            if any(values[r * cols] <= values[r * cols - 1] for r in range(1, rows)):
                continue
            matrix = [list(values[r*cols:(r+1)*cols]) for r in range(rows)]
            for target in range(-3, 5):
                check(matrix, target, target in values)
                count += 1
    print(f'74: examples, bounds, and {count} exhaustive cases passed')


if __name__ == '__main__':
    main()
