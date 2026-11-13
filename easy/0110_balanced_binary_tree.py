"""110. Balanced Binary Tree — Easy.
https://leetcode.com/problems/balanced-binary-tree/
Constraints: 0 <= nodes <= 5000; -10**4 <= node.val <= 10**4.
A tree is balanced when every node's subtree heights differ by at most one.
"""
from __future__ import annotations


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def is_balanced_straightforward(root: TreeNode | None) -> bool:
    """Recompute heights at each node: O(n*h) time, O(h) extra space."""
    def height(start):
        if start is None:
            return 0
        maximum = 0
        pending = [(start, 1)]
        while pending:
            node, depth = pending.pop()
            maximum = max(maximum, depth)
            if node.left is not None:
                pending.append((node.left, depth + 1))
            if node.right is not None:
                pending.append((node.right, depth + 1))
        return maximum

    if root is None:
        return True
    pending = [root]
    while pending:
        node = pending.pop()
        left_height = height(node.left)
        right_height = height(node.right)
        if abs(left_height - right_height) > 1:
            return False
        if node.right is not None:
            pending.append(node.right)
        if node.left is not None:
            pending.append(node.left)
    return True


def is_balanced_optimal(root: TreeNode | None) -> bool:
    """Iterative postorder: O(n) time and O(h) extra space, no recursion."""
    # Each frame records the node, continuation stage, and left height.
    frames = [(root, 0, 0)]
    returned_height = 0
    while frames:
        node, stage, left_height = frames.pop()
        if node is None:
            returned_height = 0
        elif stage == 0:
            frames.append((node, 1, 0))
            frames.append((node.left, 0, 0))
        elif stage == 1:
            # The completed left subtree returned its height.
            frames.append((node, 2, returned_height))
            frames.append((node.right, 0, 0))
        else:
            right_height = returned_height
            if abs(left_height - right_height) > 1:
                return False
            returned_height = 1 + max(left_height, right_height)
    return True


class Solution:
    def isBalanced(self, root: TreeNode | None) -> bool:
        return is_balanced_optimal(root)


def main() -> None:
    examples = [
        (None, True),
        (TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7))), True),
        (TreeNode(1, TreeNode(2, TreeNode(3, TreeNode(4), TreeNode(4)),
                               TreeNode(3)), TreeNode(2)), False),
        (TreeNode(-10000), True),
        (TreeNode(10000, None, TreeNode(0)), True),
        (TreeNode(0, None, TreeNode(0, None, TreeNode(0))), False),
    ]
    # Constraint-sized skew tests also demonstrate recursion safety.
    chain = None
    for _ in range(5000):
        chain = TreeNode(0, chain)
    examples.append((chain, False))
    nodes = [TreeNode(i % 10001) for i in range(5000)]
    for i, node in enumerate(nodes):
        if 2 * i + 1 < len(nodes):
            node.left = nodes[2 * i + 1]
        if 2 * i + 2 < len(nodes):
            node.right = nodes[2 * i + 2]
    examples.append((nodes[0], True))
    for root, expected in examples:
        assert is_balanced_straightforward(root) == expected
        assert is_balanced_optimal(root) == expected
        assert Solution().isBalanced(root) == expected
    print('110: both solutions passed examples and edge cases')


if __name__ == '__main__':
    main()
