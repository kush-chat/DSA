"""54. Spiral Matrix — Medium.
https://leetcode.com/problems/spiral-matrix/
Constraints: 1 <= rows, columns <= 10; values in [-100, 100].
"""


def spiral_straightforward(matrix: list[list[int]]) -> list[int]:
    """Simulate movement with visited cells. O(mn) time and auxiliary space."""
    rows, columns = len(matrix), len(matrix[0])
    visited = [[False] * columns for _ in range(rows)]
    directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
    row = column = direction = 0
    result = []
    for step in range(rows * columns):
        result.append(matrix[row][column])
        visited[row][column] = True
        if step == rows * columns - 1:
            break
        dr, dc = directions[direction]
        next_row, next_column = row + dr, column + dc
        if not (0 <= next_row < rows and 0 <= next_column < columns) or visited[next_row][next_column]:
            direction = (direction + 1) % 4
            dr, dc = directions[direction]
            next_row, next_column = row + dr, column + dc
        row, column = next_row, next_column
    return result


def spiral_optimal(matrix: list[list[int]]) -> list[int]:
    """Shrink four boundaries. O(mn) time, O(1) space excluding output."""
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    result = []
    while top <= bottom and left <= right:
        for column in range(left, right + 1):
            result.append(matrix[top][column])
        top += 1
        for row in range(top, bottom + 1):
            result.append(matrix[row][right])
        right -= 1
        # Guard the final single row/column against being visited twice.
        if top <= bottom:
            for column in range(right, left - 1, -1):
                result.append(matrix[bottom][column])
            bottom -= 1
        if left <= right:
            for row in range(bottom, top - 1, -1):
                result.append(matrix[row][left])
            left += 1
    return result


class Solution:
    def spiralOrder(self, matrix: list[list[int]]) -> list[int]:
        return spiral_optimal(matrix)


def main() -> None:
    from itertools import product

    def oracle(matrix: list[list[int]]) -> list[int]:
        # Peel a row, then rotate the remainder counterclockwise.
        remaining = [row.copy() for row in matrix]
        answer = []
        while remaining:
            answer.extend(remaining.pop(0))
            remaining = [list(row) for row in zip(*remaining)][::-1]
        return answer

    def check(matrix: list[list[int]], expected: list[int]) -> None:
        before = [row.copy() for row in matrix]
        for solve in (spiral_straightforward, spiral_optimal, Solution().spiralOrder):
            assert solve(matrix) == expected
            assert matrix == before

    check([[1,2,3],[4,5,6],[7,8,9]], [1,2,3,6,9,8,7,4,5])
    check([[1,2,3,4],[5,6,7,8],[9,10,11,12]], [1,2,3,4,8,12,11,10,9,5,6,7])
    checked = 0
    for rows in range(1, 11):
        for columns in range(1, 11):
            matrix = [[r*columns+c for c in range(columns)] for r in range(rows)]
            check(matrix, oracle(matrix))
            checked += 1
    for rows, columns in ((1,1), (1,4), (4,1), (2,3), (3,2), (3,3)):
        for values in product((-100, 100), repeat=rows*columns):
            matrix = [list(values[r*columns:(r+1)*columns]) for r in range(rows)]
            check(matrix, oracle(matrix))
            checked += 1
    print(f'Spiral Matrix: {checked} shape/value cases and examples passed')


if __name__ == '__main__':
    main()
