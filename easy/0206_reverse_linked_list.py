"""LeetCode 206: Reverse Linked List (Easy).

https://leetcode.com/problems/reverse-linked-list/
Reverse an acyclic singly linked list and return its new head.
Constraints: 0..5000 nodes; -5000 <= node values <= 5000.
Both solutions reuse nodes and change their next pointers.
"""
from __future__ import annotations


class ListNode:
    def __init__(self, val: int = 0, next: ListNode | None = None):
        self.val = val
        self.next = next


def reverse_list_lengthy(head: ListNode | None) -> ListNode | None:
    """Collect nodes and reconnect backwards. Time: O(n). Space: O(n)."""
    nodes: list[ListNode] = []
    current = head
    while current is not None:
        nodes.append(current)
        current = current.next
    if not nodes:
        return None
    for index in range(len(nodes) - 1, 0, -1):
        nodes[index].next = nodes[index - 1]
    nodes[0].next = None  # The former head is now the tail.
    return nodes[-1]


def reverse_list_optimal(head: ListNode | None) -> ListNode | None:
    """Reverse links in one pass. Time: O(n). Extra space: O(1)."""
    previous = None
    current = head
    while current is not None:
        following = current.next  # Save the unreversed suffix before rewiring.
        current.next = previous
        previous = current
        current = following
    return previous


class Solution:
    def reverseList(self, head: ListNode | None) -> ListNode | None:
        return reverse_list_optimal(head)


def build_list(values: list[int]) -> ListNode | None:
    head = None
    for value in reversed(values):
        head = ListNode(value, head)
    return head


def to_values(head: ListNode | None) -> list[int]:
    values = []
    while head is not None:
        values.append(head.val)
        head = head.next
    return values


def main() -> None:
    for values in [[], [1], [1, 2], [1, 2, 3, 4, 5], [2, 2, 2], [-5000, 0, 5000]]:
        # Each mutating approach gets its own freshly built input.
        lengthy = to_values(reverse_list_lengthy(build_list(values)))
        optimal = to_values(reverse_list_optimal(build_list(values)))
        assert lengthy == optimal == values[::-1]
        print(f'{values=}: lengthy={lengthy}, optimal={optimal}')


if __name__ == '__main__':
    main()
