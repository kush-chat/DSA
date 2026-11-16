"""994. Rotting Oranges — Medium.
https://leetcode.com/problems/rotting-oranges/
Constraints: 1 <= rows, cols <= 10; cells are 0 (empty), 1 (fresh), or 2 (rotten).
Rot spreads to four-directional neighbors once per minute. Inputs are preserved.
"""
from collections import deque
from itertools import product


def rot_straightforward(grid: list[list[int]]) -> int:
    """Simulate synchronous rounds: O(N**2) worst-case time, O(N) space."""
    state = [row[:] for row in grid]
    rows, cols = len(state), len(state[0])
    minutes = 0
    while True:
        fresh = 0
        newly_rotten = []
        for row in range(rows):
            for col in range(cols):
                if state[row][col] != 1:
                    continue
                fresh += 1
                for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < rows and 0 <= nc < cols and state[nr][nc] == 2:
                        newly_rotten.append((row, col))
                        break
        if fresh == 0:
            return minutes
        if not newly_rotten:
            return -1
        # Apply only after the whole scan so rot cannot jump multiple cells.
        for row, col in newly_rotten:
            state[row][col] = 2
        minutes += 1


def rot_optimal(grid: list[list[int]]) -> int:
    """Multi-source BFS: O(N) time and space, N = rows*cols."""
    state = [row[:] for row in grid]
    rows, cols = len(state), len(state[0])
    queue = deque()
    fresh = 0
    for row in range(rows):
        for col in range(cols):
            if state[row][col] == 2:
                queue.append((row, col, 0))
            elif state[row][col] == 1:
                fresh += 1
    minutes = 0
    while queue:
        row, col, minutes = queue.popleft()
        for nr, nc in ((row-1, col), (row+1, col), (row, col-1), (row, col+1)):
            if 0 <= nr < rows and 0 <= nc < cols and state[nr][nc] == 1:
                state[nr][nc] = 2  # Claim once, even with several rotten neighbors.
                fresh -= 1
                queue.append((nr, nc, minutes + 1))
    return minutes if fresh == 0 else -1


class Solution:
    def orangesRotting(self, grid: list[list[int]]) -> int:
        return rot_optimal(grid)


def check(grid, expected):
    original = [row[:] for row in grid]
    assert rot_straightforward(grid) == expected
    assert rot_optimal(grid) == expected
    assert Solution().orangesRotting(grid) == expected
    assert grid == original


def oracle(grid):
    """Search from each fresh orange to its closest original rotten source."""
    rows, cols = len(grid), len(grid[0])
    answer = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 1:
                continue
            queue = deque([(r, c, 0)])
            seen = {(r, c)}
            distance_to_source = None
            while queue:
                row, col, distance = queue.popleft()
                if grid[row][col] == 2:
                    distance_to_source = distance
                    break
                for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    nr, nc = row + dr, col + dc
                    if (0 <= nr < rows and 0 <= nc < cols
                            and grid[nr][nc] != 0 and (nr, nc) not in seen):
                        seen.add((nr, nc))
                        queue.append((nr, nc, distance + 1))
            if distance_to_source is None:
                return -1
            answer = max(answer, distance_to_source)
    return answer


def main() -> None:
    check([[2, 1, 1], [1, 1, 0], [0, 1, 1]], 4)
    check([[2, 1, 1], [0, 1, 1], [1, 0, 1]], -1)
    check([[0, 2]], 0)
    check([[0]], 0)
    check([[1]], -1)
    check([[2, 1, 1, 1, 2]], 2)
    check([[2, 0, 1]], -1)
    full = [[1] * 10 for _ in range(10)]
    full[0][0] = 2
    check(full, 18)
    check([[2] * 10 for _ in range(10)], 0)
    count = 0
    for values in product((0, 1, 2), repeat=6):
        grid = [list(values[:3]), list(values[3:])]
        check(grid, oracle(grid))
        count += 1
    print(f'994: examples, bounds, and {count} exhaustive grids passed')


if __name__ == '__main__':
    main()
