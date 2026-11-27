"""48. Rotate Image — Medium.
https://leetcode.com/problems/rotate-image/
Constraints: square matrix, 1 <= n <= 20; values in [-1000, 1000].
Both solutions rotate clockwise in-place without allocating another matrix.
"""


def rotate_straightforward(matrix: list[list[int]]) -> None:
    """Move four cells at a time, layer by layer. O(n**2) time, O(1) space."""
    n = len(matrix)
    for layer in range(n // 2):
        first = layer
        last = n - 1 - layer
        for column in range(first, last):
            offset = column - first
            top = matrix[first][column]
            # Left -> top, bottom -> left, right -> bottom, saved top -> right.
            matrix[first][column] = matrix[last - offset][first]
            matrix[last - offset][first] = matrix[last][last - offset]
            matrix[last][last - offset] = matrix[column][last]
            matrix[column][last] = top


def rotate_optimal(matrix: list[list[int]]) -> None:
    """Transpose then reverse rows. O(n**2) time, O(1) auxiliary space."""
    n = len(matrix)
    for row in range(n):
        for column in range(row + 1, n):
            matrix[row][column], matrix[column][row] = matrix[column][row], matrix[row][column]
    for row in matrix:
        row.reverse()
    # (r,c) -> (c,r) -> (c,n-1-r), exactly the clockwise mapping.


class Solution:
    def rotate(self, matrix: list[list[int]]) -> None:
        rotate_optimal(matrix)


def main() -> None:
    from itertools import product
    from random import Random

    def check(original: list[list[int]]) -> None:
        n = len(original)
        expected = [[original[n - 1 - c][r] for c in range(n)] for r in range(n)]
        for solve in (rotate_straightforward, rotate_optimal, Solution().rotate):
            matrix = [row.copy() for row in original]
            row_aliases = matrix.copy()
            assert solve(matrix) is None
            assert matrix == expected
            assert all(matrix[i] is row_aliases[i] for i in range(n))
            for _ in range(3):
                solve(matrix)
            assert matrix == original  # Four turns restore every cell.

    check([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    check([[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]])
    check([[-1000]])
    checked = 0
    for n in range(1, 4):
        for values in product((-1, 1), repeat=n*n):
            check([list(values[r*n:(r+1)*n]) for r in range(n)])
            checked += 1
    rng = Random(48)
    for n in range(1, 21):
        check([[r*n+c for c in range(n)] for r in range(n)])
        check([[rng.randint(-1000, 1000) for _ in range(n)] for _ in range(n)])
    print(f'Rotate Image: {checked} exhaustive matrices, all sizes, and examples passed')


if __name__ == '__main__':
    main()
