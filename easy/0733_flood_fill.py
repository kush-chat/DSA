"""LeetCode 733: Flood Fill (Easy).

https://leetcode.com/problems/flood-fill/
Recolor the starting pixel's four-directionally connected color region.
Constraints: 1..50 rows/columns; colors in 0..65535; start is within the image.
Both approaches modify and return the input image. For N pixels, both take O(N)
time and O(N) worst-case extra space; the optimal version avoids a visited set.
"""
from collections import deque


def flood_fill_lengthy(image: list[list[int]], sr: int, sc: int,
                       color: int) -> list[list[int]]:
    """BFS with explicit visited tracking: O(N) time and extra space."""
    rows, cols = len(image), len(image[0])
    original = image[sr][sc]
    visited = {(sr, sc)}
    queue = deque([(sr, sc)])
    while queue:
        row, col = queue.popleft()
        image[row][col] = color
        for nr, nc in [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]:
            if (0 <= nr < rows and 0 <= nc < cols
                    and (nr, nc) not in visited and image[nr][nc] == original):
                visited.add((nr, nc))
                queue.append((nr, nc))
    return image


def flood_fill_optimal(image: list[list[int]], sr: int, sc: int,
                       color: int) -> list[list[int]]:
    """Iterative DFS using recoloring as visited marking: O(N) time/space."""
    original = image[sr][sc]
    if original == color:
        return image  # Otherwise recoloring would not mark a pixel as visited.
    rows, cols = len(image), len(image[0])
    image[sr][sc] = color
    stack = [(sr, sc)]
    while stack:
        row, col = stack.pop()
        for nr, nc in [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]:
            if 0 <= nr < rows and 0 <= nc < cols and image[nr][nc] == original:
                image[nr][nc] = color  # Mark before pushing to avoid duplicates.
                stack.append((nr, nc))
    return image


class Solution:
    def floodFill(self, image: list[list[int]], sr: int, sc: int,
                  color: int) -> list[list[int]]:
        return flood_fill_optimal(image, sr, sc, color)


def main() -> None:
    cases = [([[1,1,1],[1,1,0],[1,0,1]], 1, 1, 2,
              [[2,2,2],[2,2,0],[2,0,1]]),
             ([[0,0,0],[0,0,0]], 0, 0, 0, [[0,0,0],[0,0,0]]),
             ([[1,0],[0,1]], 0, 0, 2, [[2,0],[0,1]]),
             ([[65535]], 0, 0, 0, [[0]])]
    for image, sr, sc, color, expected in cases:
        lengthy = flood_fill_lengthy([r[:] for r in image], sr, sc, color)
        optimal = flood_fill_optimal([r[:] for r in image], sr, sc, color)
        assert lengthy == optimal == expected
        assert Solution().floodFill([r[:] for r in image], sr, sc, color) == expected
        print(f'lengthy={lengthy}, optimal={optimal}')


if __name__ == '__main__':
    main()
