import fileinput
from typing import List
import unittest

from main_102 import hash


def to_bin(hex: str) -> str:
    lookup = {
        '0': '0000',
        '1': '0001',
        '2': '0010',
        '3': '0011',
        '4': '0100',
        '5': '0101',
        '6': '0110',
        '7': '0111',
        '8': '1000',
        '9': '1001',
        'a': '1010',
        'b': '1011',
        'c': '1100',
        'd': '1101',
        'e': '1110',
        'f': '1111'
    }
    return ''.join(lookup[x] for x in hex)


def build_map(key: str) -> List[List[int]]:
    out = []  # type: List[List[int]]
    for i in range(128):
        h = hash('{}-{}'.format(key, i))
        b = to_bin(h)
        out += [[int(x) for x in b]]
    return out


def count_used(map: List[List[int]]) -> int:
    total = 0
    for line in map:
        for cell in line:
            if cell == 1:
                total += 1
    return total


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines += [line.strip()]
    print(count_used(build_map(lines[0])))


class Tests141(unittest.TestCase):
    def test_to_bin_1(self):
        self.assertEqual('0000', to_bin('0'))

    def test_to_bin_2(self):
        self.assertEqual('0001', to_bin('1'))

    def test_to_bin_3(self):
        self.assertEqual('1110', to_bin('e'))

    def test_to_bin_4(self):
        self.assertEqual('1111', to_bin('f'))

    def test_to_bin_5(self):
        self.assertEqual('1010000011000010000000010111', to_bin('a0c2017'))

    def test(self):
        self.assertEqual(8108, count_used(build_map('flqrgnkx')))
