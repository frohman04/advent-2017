import fileinput
from typing import List
import unittest


def is_valid(passphrase: str) -> bool:
    seen = set([])
    for word in passphrase.split():
        if word not in seen:
            seen.add(word)
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


class Tests041(unittest.TestCase):
    def test_1(self):
        self.assertEqual(is_valid('aa bb cc dd ee'), True)

    def test_2(self):
        self.assertEqual(is_valid('aa bb cc dd aa'), False)

    def test_3(self):
        self.assertEqual(is_valid('aa bb cc dd aaa'), True)

    def test_4(self):
        self.assertEqual(num_valid(['aa bb cc dd ee', 'aa bb cc dd aa', 'aa bb cc dd aaa']), 2)
