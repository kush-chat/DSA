"""LeetCode 104: Maximum Depth of Binary Tree (Easy).

https://leetcode.com/problems/maximum-depth-of-binary-tree/
Return the greatest root-to-leaf path length in nodes.
Constraints: 0..10_000 nodes; values -100..100. Neither approach mutates the tree.
Both are linear-time interview solutions; DFS uses height-bounded storage,
whereas the more explicit level-order approach uses width-bounded storage.
"""
from __future__ import annotations
from collections import deque


class TreeNode:
    def __init__(self, val: int = 0, left: TreeNode | None = None,
                 right: TreeNode | None = None):
        self.val, self.left, self.right = val, left, right


def max_depth_lengthy(root: TreeNode | None) -> int:
    """Count BFS levels. Time: O(n). Extra space: O(w), maximum tree width."""
    if root is None:
        return 0
    queue = deque([root])
    depth = 0
    while queue:
        level_size = len(queue)
        for _ in range(level_size):
            node = queue.popleft()
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        depth += 1
    return depth


def max_depth_optimal(root: TreeNode | None) -> int:
    """Iterative DFS. Time: O(n). Extra space: O(h), tree height."""
    if root is None:
        return 0
    stack = [(root, 1)]
    deepest = 0
    while stack:
        node, depth = stack.pop()
        deepest = max(deepest, depth)
        # An explicit stack avoids Python's recursion limit on deep trees.
        if node.right is not None:
            stack.append((node.right, depth + 1))
        if node.left is not None:
            stack.append((node.left, depth + 1))
    return deepest


class Solution:
    def maxDepth(self, root: TreeNode | None) -> int:
        return max_depth_optimal(root)


def main() -> None:
    cases = [(None, 0), (TreeNode(1), 1), (TreeNode(1, right=TreeNode(2)), 2),
             (TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7))), 3),
             (TreeNode(0, TreeNode(0, TreeNode(0))), 3)]
    for root, expected in cases:
        lengthy = max_depth_lengthy(root)
        optimal = max_depth_optimal(root)
        assert lengthy == optimal == expected
        print(f'expected={expected}: lengthy={lengthy}, optimal={optimal}')


if __name__ == '__main__':
    main()
