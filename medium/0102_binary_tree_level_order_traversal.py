"""102. Binary Tree Level Order Traversal — Medium.
https://leetcode.com/problems/binary-tree-level-order-traversal/
Constraints: 0 <= nodes <= 2000; -1000 <= node.val <= 1000.
Return node values grouped by depth, ordered left to right within each depth.
"""
from __future__ import annotations
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def level_order_straightforward(root: TreeNode | None) -> list[list[int]]:
    """Scan each depth separately: O(n*h) time, O(h) space plus O(n) output."""
    if root is None:
        return []
    # First discover the number of levels without recursive calls.
    height = 0
    pending = [(root, 0)]
    while pending:
        node, depth = pending.pop()
        height = max(height, depth + 1)
        if node.right is not None:
            pending.append((node.right, depth + 1))
        if node.left is not None:
            pending.append((node.left, depth + 1))

    result = []
    for target in range(height):
        level = []
        pending = [(root, 0)]
        while pending:
            node, depth = pending.pop()
            if depth == target:
                level.append(node.val)
                continue
            # Push right first so the left subtree is visited first.
            if node.right is not None:
                pending.append((node.right, depth + 1))
            if node.left is not None:
                pending.append((node.left, depth + 1))
        result.append(level)
    return result


def level_order_optimal(root: TreeNode | None) -> list[list[int]]:
    """Breadth-first traversal: O(n) time, O(w) space plus O(n) output."""
    if root is None:
        return []
    queue = deque([root])
    result = []
    while queue:
        level = []
        # Snapshot this level's size before adding next-level children.
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        result.append(level)
    return result


class Solution:
    def levelOrder(self, root: TreeNode | None) -> list[list[int]]:
        return level_order_optimal(root)


def main() -> None:
    cases = [
        (None, []),
        (TreeNode(1), [[1]]),
        (TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7))),
         [[3], [9, 20], [15, 7]]),
        (TreeNode(0, TreeNode(-1000, None, TreeNode(2)),
                     TreeNode(1000, TreeNode(3))), [[0], [-1000, 1000], [2, 3]]),
    ]
    chain = None
    for i in reversed(range(2000)):
        chain = TreeNode(i % 1001, None, chain)
    cases.append((chain, [[i % 1001] for i in range(2000)]))
    nodes = [TreeNode(i % 1001) for i in range(2000)]
    for i, node in enumerate(nodes):
        if 2 * i + 1 < len(nodes):
            node.left = nodes[2 * i + 1]
        if 2 * i + 2 < len(nodes):
            node.right = nodes[2 * i + 2]
    expected = []
    start, width = 0, 1
    while start < len(nodes):
        expected.append([i % 1001 for i in range(start, min(start + width, len(nodes)))])
        start += width
        width *= 2
    cases.append((nodes[0], expected))
    for root, expected in cases:
        assert level_order_straightforward(root) == expected
        assert level_order_optimal(root) == expected
        assert Solution().levelOrder(root) == expected
    print('102: both solutions passed examples and edge cases')


if __name__ == '__main__':
    main()
