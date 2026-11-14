"""21. Merge Two Sorted Lists — Easy.
https://leetcode.com/problems/merge-two-sorted-lists/
Each list has 0..50 nodes with values in [-100, 100], sorted nondecreasingly.
Both implementations splice existing nodes and mutate the input links.
"""
from __future__ import annotations
from itertools import combinations_with_replacement


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def merge_straightforward(list1: ListNode | None,
                          list2: ListNode | None) -> ListNode | None:
    """Collect, sort, and relink nodes: O(N log N) time, O(N) extra space."""
    nodes = []
    current = list1
    while current is not None:
        nodes.append(current)
        current = current.next
    current = list2
    while current is not None:
        nodes.append(current)
        current = current.next
    if not nodes:
        return None

    # Keep the node objects rather than copying values into new nodes.
    nodes.sort(key=lambda node: node.val)
    for index in range(len(nodes) - 1):
        nodes[index].next = nodes[index + 1]
    nodes[-1].next = None
    return nodes[0]


def merge_optimal(list1: ListNode | None,
                  list2: ListNode | None) -> ListNode | None:
    """Two pointers: O(N) worst-case time, O(1) extra space; N = total nodes."""
    dummy = ListNode()
    tail = dummy
    while list1 is not None and list2 is not None:
        # Each head is the smallest remaining value in its own list.
        if list1.val <= list2.val:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next
        tail = tail.next
    # The remaining suffix is already sorted, so attach it in one step.
    tail.next = list1 if list1 is not None else list2
    return dummy.next


class Solution:
    def mergeTwoLists(self, list1: ListNode | None,
                      list2: ListNode | None) -> ListNode | None:
        return merge_optimal(list1, list2)


def build(values):
    nodes = [ListNode(value) for value in values]
    for left, right in zip(nodes, nodes[1:]):
        left.next = right
    return (nodes[0] if nodes else None), nodes


def check(left, right, expected):
    for solve in (merge_straightforward, merge_optimal, Solution().mergeTwoLists):
        # Fresh inputs matter because both implementations change links.
        head1, nodes1 = build(left)
        head2, nodes2 = build(right)
        current = solve(head1, head2)
        seen = set()
        actual = []
        while current is not None:
            assert current not in seen, 'Output contains a cycle'
            seen.add(current)
            actual.append(current.val)
            current = current.next
        assert actual == expected, (left, right, actual, expected)
        assert seen == set(nodes1 + nodes2), 'Every input node must be reused'


def main() -> None:
    cases = [
        ([1, 2, 4], [1, 3, 4], [1, 1, 2, 3, 4, 4]),
        ([], [], []),
        ([], [0], [0]),
        ([0], [], [0]),
        ([-100, -100], [100, 100], [-100, -100, 100, 100]),
        ([1, 1], [1, 1], [1, 1, 1, 1]),
    ]
    for left, right, expected in cases:
        check(left, right, expected)
    left = list(range(-100, 0, 2))
    right = list(range(-99, 1, 2))
    check(left, right, list(range(-100, 0)))
    check([100] * 50, [-100] * 50, [-100] * 50 + [100] * 50)

    arrays = [values for size in range(6)
              for values in combinations_with_replacement((-1, 0, 1), size)]
    for left in arrays:
        for right in arrays:
            check(left, right, sorted(left + right))
    print(f'21: examples, bounds, and {len(arrays)**2} exhaustive pairs passed')


if __name__ == '__main__':
    main()
