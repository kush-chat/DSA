"""LeetCode 200: Number of Islands (Medium).

https://leetcode.com/problems/number-of-islands/
Count four-directionally connected land components.
Constraints: 1..300 rows/columns; cells are '0' (water) or '1' (land).
Both approaches preserve the input. Let N be the number of cells.
"""


def num_islands_lengthy(grid: list[list[str]]) -> int:
    """Union-find: O(N * alpha(N)) amortized time, O(N) extra space."""
    rows, cols = len(grid), len(grid[0])
    parent = list(range(rows * cols))
    size = [1] * (rows * cols)
    count = sum(cell == '1' for row in grid for cell in row)

    def find(node: int) -> int:
        while node != parent[node]:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] != '1':
                continue
            # Up and left suffice to process each undirected edge once.
            for nr, nc in [(row-1, col), (row, col-1)]:
                if nr >= 0 and nc >= 0 and grid[nr][nc] == '1':
                    a, b = find(row * cols + col), find(nr * cols + nc)
                    if a != b:
                        if size[a] < size[b]:
                            a, b = b, a
                        parent[b] = a
                        size[a] += size[b]
                        count -= 1
    return count


def num_islands_optimal(grid: list[list[str]]) -> int:
    """Iterative DFS: O(N) time and O(N) extra space, including the copy."""
    cells = [row[:] for row in grid]
    rows, cols = len(cells), len(cells[0])
    count = 0
    for row in range(rows):
        for col in range(cols):
            if cells[row][col] != '1':
                continue
            count += 1
            cells[row][col] = '0'
            stack = [(row, col)]
            while stack:
                r, c = stack.pop()
                for nr, nc in [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]:
                    if 0 <= nr < rows and 0 <= nc < cols and cells[nr][nc] == '1':
                        cells[nr][nc] = '0'  # Mark on discovery, not on removal.
                        stack.append((nr, nc))
    return count


class Solution:
    def numIslands(self, grid: list[list[str]]) -> int:
        return num_islands_optimal(grid)


def main() -> None:
    cases = [(['11110','11010','11000','00000'], 1),
             (['11000','11000','00100','00011'], 3),
             (['0'], 0), (['1'], 1), (['10','01'], 2),
             (['10101'], 3), (['111','101','111'], 1)]
    for rows, expected in cases:
        grid = [list(row) for row in rows]
        before = [row[:] for row in grid]
        lengthy = num_islands_lengthy(grid)
        optimal = num_islands_optimal(grid)
        assert lengthy == optimal == expected
        assert Solution().numIslands(grid) == expected
        assert grid == before
        print(f'lengthy={lengthy}, optimal={optimal}')


if __name__ == '__main__':
    main()
