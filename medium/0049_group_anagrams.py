"""LeetCode 49: Group Anagrams (Medium).

https://leetcode.com/problems/group-anagrams/
Group words with identical letter multiplicities; group order does not matter.
Constraints: 1..10_000 words; word lengths 0..100; lowercase English letters.
Neither approach changes the input. N is word count; K is maximum word length.
"""


def group_anagrams_lengthy(strs: list[str]) -> list[list[str]]:
    """Group by sorted spelling. Time: O(N*K*log(K+1)+N). Space: O(N*(K+1))."""
    groups: dict[str, list[str]] = {}
    for word in strs:
        sorted_letters = sorted(word)
        key = ''.join(sorted_letters)
        if key not in groups:
            groups[key] = []
        groups[key].append(word)
    return list(groups.values())


def group_anagrams_optimal(strs: list[str]) -> list[list[str]]:
    """Group by counts. Expected time: O(N*(K+26)). Extra space: O(26*N)."""
    groups: dict[tuple[int, ...], list[str]] = {}
    for word in strs:
        counts = [0] * 26
        for char in word:
            counts[ord(char) - ord('a')] += 1
        # Immutable tuples are hashable; counts also distinguish repeated letters.
        key = tuple(counts)
        groups.setdefault(key, []).append(word)
    # Lists store references to the original strings rather than copying them.
    return list(groups.values())


class Solution:
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        return group_anagrams_optimal(strs)


def main() -> None:
    cases = [(['eat', 'tea', 'tan', 'ate', 'nat', 'bat'],
              [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]),
             ([''], [['']]), (['a'], [['a']]),
             (['', '', 'a'], [['', ''], ['a']]),
             (['ab', 'ba', 'ab', 'aab', 'abb'], [['ab', 'ba', 'ab'], ['aab'], ['abb']])]
    def normalize(groups: list[list[str]]) -> list[list[str]]:
        return sorted(sorted(group) for group in groups)

    for words, expected in cases:
        lengthy = group_anagrams_lengthy(words)
        optimal = group_anagrams_optimal(words)
        assert normalize(lengthy) == normalize(optimal) == normalize(expected)
        print(f'{words=}: lengthy={lengthy}, optimal={optimal}')


if __name__ == '__main__':
    main()
