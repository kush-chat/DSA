"""542. 01 Matrix — Medium.
https://leetcode.com/problems/01-matrix/
Constraints: 1 <= rows, cols <= 10000; rows*cols <= 10000;
entries are 0 or 1, and at least one zero exists. Inputs are not mutated.
"""
from collections import deque
from itertools import product


def distances_straightforward(mat: list[list[int]]) -> list[list[int]]:
    """Compare every one with every zero: O(N*Z) time, O(N) space including output."""
    rows, cols = len(mat), len(mat[0])
    zeros = []
    for row in range(rows):
        for col in range(cols):
            if mat[row][col] == 0:
                zeros.append((row, col))
    result = [[0] * cols for _ in range(rows)]
    for row in range(rows):
        for col in range(cols):
            if mat[row][col] == 0:
                continue
            closest = rows + cols
            for zero_row, zero_col in zeros:
                # There are no obstacles, so Manhattan distance is attainable.
                vertical = abs(row - zero_row)
                horizontal = abs(col - zero_col)
                candidate = vertical + horizontal
                if candidate < closest:
                    closest = candidate
            result[row][col] = closest
    return result


def distances_optimal(mat: list[list[int]]) -> list[list[int]]:
    """Multi-source BFS: O(N) time and space, N = rows*cols."""
    rows, cols = len(mat), len(mat[0])
    result = [[-1] * cols for _ in range(rows)]
    queue = deque()
    for row in range(rows):
        for col in range(cols):
            if mat[row][col] == 0:
                result[row][col] = 0
                queue.append((row, col))
    while queue:
        row, col = queue.popleft()
        for nr, nc in ((row-1, col), (row+1, col), (row, col-1), (row, col+1)):
            if 0 <= nr < rows and 0 <= nc < cols and result[nr][nc] == -1:
                # The first arrival is shortest; mark before enqueueing.
                result[nr][nc] = result[row][col] + 1
                queue.append((nr, nc))
    return result


class Solution:
    def updateMatrix(self, mat: list[list[int]]) -> list[list[int]]:
        return distances_optimal(mat)


def check(mat, expected):
    original = [row[:] for row in mat]
    assert distances_straightforward(mat) == expected
    assert distances_optimal(mat) == expected
    assert Solution().updateMatrix(mat) == expected
    assert mat == original


def search_oracle(mat):
    """Independent BFS from each cell, stopping at the first zero."""
    rows, cols = len(mat), len(mat[0])
    result = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            queue = deque([(r, c, 0)])
            seen = {(r, c)}
            while queue:
                row, col, distance = queue.popleft()
                if mat[row][col] == 0:
                    result[r][c] = distance
                    break
                for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in seen:
                        seen.add((nr, nc))
                        queue.append((nr, nc, distance + 1))
    return result


def main() -> None:
    check([[0, 0, 0], [0, 1, 0], [0, 0, 0]], [[0, 0, 0], [0, 1, 0], [0, 0, 0]])
    check([[0, 0, 0], [0, 1, 0], [1, 1, 1]], [[0, 0, 0], [0, 1, 0], [1, 2, 1]])
    check([[0]], [[0]])
    check([[0] + [1] * 9999], [list(range(10000))])
    check([[0]] + [[1] for _ in range(9999)], [[i] for i in range(10000)])
    check([[0] * 100 for _ in range(100)], [[0] * 100 for _ in range(100)])
    count = 0
    for bits in product((0, 1), repeat=9):
        if 0 not in bits:
            continue
        mat = [list(bits[i:i+3]) for i in range(0, 9, 3)]
        check(mat, search_oracle(mat))
        count += 1
    print(f'542: examples, maximum dimensions, and {count} exhaustive matrices passed')


if __name__ == '__main__':
    main()
