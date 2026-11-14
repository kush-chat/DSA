"""19. Remove Nth Node From End of List — Medium.
https://leetcode.com/problems/remove-nth-node-from-end-of-list/
Constraints: 1 <= size <= 30; 0 <= node.val <= 100; 1 <= n <= size.
Both solutions mutate links while retaining the surviving input nodes.
"""
from __future__ import annotations
from itertools import product


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def remove_straightforward(head: ListNode, n: int) -> ListNode | None:
    """Count then locate the predecessor: O(L) time, O(1) extra space."""
    length = 0
    current = head
    while current is not None:
        length += 1
        current = current.next

    index_from_start = length - n
    if index_from_start == 0:
        return head.next

    # Stop one node before the zero-based removal index.
    previous = head
    position = 0
    while position < index_from_start - 1:
        previous = previous.next
        position += 1
    removed = previous.next
    previous.next = removed.next
    return head


def remove_optimal(head: ListNode, n: int) -> ListNode | None:
    """One pass with a fixed pointer gap: O(L) time, O(1) extra space."""
    dummy = ListNode(0, head)
    slow = fast = dummy
    for _ in range(n):
        fast = fast.next
    # The n-link gap places slow just before the target when fast is last.
    while fast.next is not None:
        slow = slow.next
        fast = fast.next
    slow.next = slow.next.next
    # The sentinel makes removing the head identical to any other removal.
    return dummy.next


class Solution:
    def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode | None:
        return remove_optimal(head, n)


def check(values, n, expected):
    for solve in (remove_straightforward, remove_optimal, Solution().removeNthFromEnd):
        nodes = [ListNode(value) for value in values]
        for left, right in zip(nodes, nodes[1:]):
            left.next = right
        result = solve(nodes[0], n)
        actual_nodes = []
        seen = set()
        while result is not None:
            assert result not in seen, 'Output contains a cycle'
            seen.add(result)
            actual_nodes.append(result)
            result = result.next
        index = len(values) - n
        assert actual_nodes == nodes[:index] + nodes[index + 1:]
        assert [node.val for node in actual_nodes] == expected


def main() -> None:
    check([1, 2, 3, 4, 5], 2, [1, 2, 3, 5])
    check([1], 1, [])
    check([1, 2], 1, [1])
    check([1, 2], 2, [2])
    check([0, 100, 0], 2, [0, 0])
    count = 0
    for length in range(1, 8):
        for values in product((0, 1), repeat=length):
            for n in range(1, length + 1):
                index = length - n
                expected = list(values[:index] + values[index + 1:])
                check(values, n, expected)
                count += 1
    values = [0, 100] * 15
    for n in range(1, 31):
        index = len(values) - n
        check(values, n, values[:index] + values[index + 1:])
    print(f'19: examples, all maximum-size removals, and {count} exhaustive cases passed')


if __name__ == '__main__':
    main()
