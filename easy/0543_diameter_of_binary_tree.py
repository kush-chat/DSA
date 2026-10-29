"""LeetCode 543: Diameter of Binary Tree (Easy).

https://leetcode.com/problems/diameter-of-binary-tree/
Return the longest path between any two nodes, measured in edges.
Constraints: 1..10_000 nodes; values -100..100. Trees are not mutated.
The quadratic baseline is educational; use postorder processing for large trees.
"""
from __future__ import annotations


class TreeNode:
    def __init__(self, val: int = 0, left: TreeNode | None = None,
                 right: TreeNode | None = None):
        self.val, self.left, self.right = val, left, right


def subtree_height(root: TreeNode | None) -> int:
    if root is None:
        return 0
    stack = [(root, 1)]
    height = 0
    while stack:
        node, depth = stack.pop()
        height = max(height, depth)
        if node.left is not None:
            stack.append((node.left, depth + 1))
        if node.right is not None:
            stack.append((node.right, depth + 1))
    return height


def diameter_lengthy(root: TreeNode | None) -> int:
    """Recompute child heights at every node. Time: O(n²). Space: O(h)."""
    if root is None:
        return 0
    stack = [root]
    best = 0
    while stack:
        node = stack.pop()
        best = max(best, subtree_height(node.left) + subtree_height(node.right))
        if node.left is not None:
            stack.append(node.left)
        if node.right is not None:
            stack.append(node.right)
    return best


def diameter_optimal(root: TreeNode | None) -> int:
    """Iterative postorder with cached heights. Time: O(n). Extra space: O(n)."""
    if root is None:
        return 0
    heights: dict[TreeNode, int] = {}
    stack = [(root, False)]
    best = 0
    while stack:
        node, ready = stack.pop()
        if ready:
            left = heights.get(node.left, 0)
            right = heights.get(node.right, 0)
            # Child heights count nodes; their sum counts edges through this node.
            best = max(best, left + right)
            heights[node] = 1 + max(left, right)
        else:
            stack.append((node, True))
            if node.right is not None:
                stack.append((node.right, False))
            if node.left is not None:
                stack.append((node.left, False))
    return best


class Solution:
    def diameterOfBinaryTree(self, root: TreeNode | None) -> int:
        return diameter_optimal(root)


def main() -> None:
    cases = [(TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3)), 3),
             (TreeNode(1, TreeNode(2)), 1), (TreeNode(1), 0),
             (TreeNode(0, TreeNode(0, TreeNode(0, TreeNode(0)),
                                    TreeNode(0, right=TreeNode(0)))), 4)]
    for root, expected in cases:
        lengthy = diameter_lengthy(root)
        optimal = diameter_optimal(root)
        assert lengthy == optimal == expected
        print(f'expected={expected}: lengthy={lengthy}, optimal={optimal}')


if __name__ == '__main__':
    main()
