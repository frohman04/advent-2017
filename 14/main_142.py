from collections import deque
import fileinput
from typing import List, Tuple, Set
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


def build_map(key: str) -> List[List[bool]]:
    out = []  # type: List[List[bool]]
    for i in range(128):
        h = hash('{}-{}'.format(key, i))
        b = to_bin(h)
        out += [[x == '1' for x in b]]
    return out


def explore_region(used_map: List[List[bool]], start: Tuple[int, int]) -> Set[Tuple[int, int]]:
    if not used_map[start[0]][start[1]]:
        return set([])
    else:
        to_explore = deque([start])
        in_region = set([])
        while len(to_explore) > 0:
            loc = to_explore.pop()
            in_region.add(loc)
            for diff in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next = (loc[0] + diff[0], loc[1] + diff[1])
                if (next not in in_region and
                        0 <= next[0] < len(used_map) and
                        0 <= next[1] < len(used_map[loc[0]]) and
                        used_map[next[0]][next[1]]):
                    to_explore.appendleft(next)
        return in_region


def count_regions(used_map: List[List[bool]]) -> int:
    in_region = set([])  # type: Set[Tuple[int, int]]
    region_count = 0
    for x in range(len(used_map)):
        for y in range(len(used_map[x])):
            if (x, y) not in in_region:
                region_cells = explore_region(used_map, (x, y))
                if len(region_cells) > 0:
                    region_count += 1
                    in_region.update(region_cells)
                    for cell in region_cells:
                        used_map[cell[0]][cell[1]] = False
    return region_count


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines += [line.strip()]
    print(count_regions(build_map(lines[0])))


class Tests142(unittest.TestCase):
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

    def test_explore_region_empty(self):
        self.assertEqual(set([]), explore_region([[False]], (0, 0)))

    def test_explore_region_single(self):
        self.assertEqual(set([(0, 0)]), explore_region([[True]], (0, 0)))

    def test_explore_region_x(self):
        self.assertEqual(set([(1, 0), (2, 0), (3, 0)]),
                         explore_region([[False], [True], [True], [True], [False]], (2, 0)))

    def test_explore_region_y(self):
        self.assertEqual(set([(0, 1), (0, 2), (0, 3)]),
                         explore_region([[False, True, True, True, False]], (0, 2)))

    def test_explore_region_square(self):
        self.assertEqual(set([(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)]),
                         explore_region([[False, False, False, False, False],
                                         [False, True, True, True, False],
                                         [False, True, True, True, False],
                                         [False, True, True, True, False],
                                         [False, False, False, False, False]],
                                        (2, 2)))

    def test_explore_region_ignore_diagonal(self):
        self.assertEqual(set([(1, 1)]),
                         explore_region([[True, False, True],
                                         [False, True, False],
                                         [True, False, True]],
                                        (1, 1)))

    def test_count_regions_empty(self):
        self.assertEqual(0, count_regions([[]]))

    def test_count_regions_single(self):
        self.assertEqual(1, count_regions([[True]]))

    def test_count_regions_two_x(self):
        self.assertEqual(2, count_regions([[True], [False], [True]]))

    def test_count_regions_two_y(self):
        self.assertEqual(2, count_regions([[True, False, True]]))

    def test(self):
        self.assertEqual(1242, count_regions(build_map('flqrgnkx')))
