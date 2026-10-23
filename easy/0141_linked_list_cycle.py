"""LeetCode 141: Linked List Cycle (Easy).

https://leetcode.com/problems/linked-list-cycle/
Determine whether following next pointers eventually revisits a node.
Constraints: 0..10_000 nodes; -100_000 <= node values <= 100_000.
Neither solution changes the list. The cycle position is only a test fixture;
LeetCode passes the head, not the position, to the solution.
"""
from __future__ import annotations


class ListNode:
    def __init__(self, val: int = 0, next: ListNode | None = None):
        self.val = val
        self.next = next


def has_cycle_lengthy(head: ListNode | None) -> bool:
    """Remember visited node identities. Expected time: O(n). Space: O(n)."""
    visited: set[ListNode] = set()
    current = head
    while current is not None:
        if current in visited:
            return True
        visited.add(current)
        current = current.next
    return False


def has_cycle_optimal(head: ListNode | None) -> bool:
    """Floyd's slow/fast pointers. Time: O(n). Extra space: O(1)."""
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        # Inside a cycle the fast pointer gains one node per iteration.
        # Compare node identity, since separate nodes can hold equal values.
        if slow is fast:
            return True
    return False


class Solution:
    def hasCycle(self, head: ListNode | None) -> bool:
        return has_cycle_optimal(head)


def build_list(values: list[int], pos: int = -1) -> ListNode | None:
    nodes = [ListNode(value) for value in values]
    for index in range(len(nodes) - 1):
        nodes[index].next = nodes[index + 1]
    if nodes and pos >= 0:
        nodes[-1].next = nodes[pos]
    return nodes[0] if nodes else None


def main() -> None:
    cases = [([3, 2, 0, -4], 1), ([1, 2], 0), ([1], -1),
             ([], -1), ([1], 0), ([7, 7, 7], -1), ([7, 7, 7], 2)]
    for values, pos in cases:
        head = build_list(values, pos)
        lengthy = has_cycle_lengthy(head)
        optimal = has_cycle_optimal(head)
        assert lengthy == optimal == (pos >= 0)
        print(f'{values=}, {pos=}: lengthy={lengthy}, optimal={optimal}')


if __name__ == '__main__':
    main()
