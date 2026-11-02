"""LeetCode 347: Top K Frequent Elements (Medium).

https://leetcode.com/problems/top-k-frequent-elements/
Return the k most frequent distinct values, in any order.
Constraints: 1 <= len(nums) <= 100_000; -10_000 <= nums[i] <= 10_000;
1 <= k <= number of unique values; the answer set is unique.
Both approaches preserve the input. Hash operations have expected O(1) cost.
"""


def top_k_frequent_lengthy(nums: list[int], k: int) -> list[int]:
    """Count and sort distinct values. Time O(n + u log u), space O(u)."""
    counts: dict[int, int] = {}
    for value in nums:
        counts[value] = counts.get(value, 0) + 1
    ranked = sorted(counts, key=lambda value: counts[value], reverse=True)
    return ranked[:k]


def top_k_frequent_optimal(nums: list[int], k: int) -> list[int]:
    """Frequency buckets. Expected time O(n), extra space O(n)."""
    counts: dict[int, int] = {}
    for value in nums:
        counts[value] = counts.get(value, 0) + 1
    # No frequency exceeds the input length, so sorting is unnecessary.
    buckets: list[list[int]] = [[] for _ in range(len(nums) + 1)]
    for value, frequency in counts.items():
        buckets[frequency].append(value)
    result = []
    for frequency in range(len(nums), 0, -1):
        for value in buckets[frequency]:
            result.append(value)
            if len(result) == k:
                return result
    raise AssertionError('Unreachable for valid k')


class Solution:
    def topKFrequent(self, nums: list[int], k: int) -> list[int]:
        return top_k_frequent_optimal(nums, k)


def main() -> None:
    cases = [([1, 1, 1, 2, 2, 3], 2, {1, 2}), ([1], 1, {1}),
             ([1, 2, 1, 2, 1, 2, 3, 1, 3, 2], 2, {1, 2}),
             ([-1, -1, 0], 1, {-1}), ([4, 4, 4], 1, {4}),
             ([-10000, 10000], 2, {-10000, 10000})]
    for nums, k, expected in cases:
        before = nums[:]
        lengthy = top_k_frequent_lengthy(nums, k)
        optimal = top_k_frequent_optimal(nums, k)
        assert len(lengthy) == len(optimal) == k
        assert set(lengthy) == set(optimal) == expected
        assert set(Solution().topKFrequent(nums, k)) == expected
        assert nums == before
        print(f'k={k}: lengthy={lengthy}, optimal={optimal}')


if __name__ == '__main__':
    main()
