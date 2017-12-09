from collections import defaultdict
import fileinput
from typing import Dict, List, Set, Tuple
import unittest


def build_key(passphrase: str) -> Tuple[Tuple[str, int]]:
    counts = defaultdict(lambda: 0)  # type: Dict[str, int]
    for letter in passphrase:
        counts[letter] += 1
    return tuple(sorted(dict(counts).items()))


def is_valid(passphrase: str) -> bool:
    seen = set([])  # type: Set[Dict[str, int]]
    for word in passphrase.split():
        key = build_key(word)
        if key not in seen:
            seen.add(key)
        else:
            return False
    return True


def num_valid(passphrases: List[str]) -> int:
    return len([x for x in passphrases if is_valid(x)])


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines += [line.strip()]
    print(num_valid(lines))


class Tests042(unittest.TestCase):
    def test_1(self):
        self.assertEqual(is_valid('abcde fghij'), True)

    def test_2(self):
        self.assertEqual(is_valid('abcde xyz ecdab'), False)

    def test_3(self):
        self.assertEqual(is_valid('a ab abc abd abf abj'), True)

    def test_4(self):
        self.assertEqual(is_valid('iiii oiii ooii oooi oooo'), True)

    def test_5(self):
        self.assertEqual(is_valid('oiii ioii iioi iiio'), False)

    def test_6(self):
        self.assertEqual(num_valid(['abcde fghij', 'abcde xyz ecdab', 'a ab abc abd abf abj']), 2)
