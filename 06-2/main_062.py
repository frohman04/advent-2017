import fileinput
from typing import List
import unittest


def single_rebalance(cells: List[int]) -> List[int]:
    idx = -max(zip(cells, [-x for x in range(len(cells))]))[1]

    remaining = cells[idx]
    cells[idx] = 0
    while remaining > 0:
        idx += 1
        if idx == len(cells):
            idx = 0
        cells[idx] += 1
        remaining -= 1

    return cells


def rebalance(cells: List[int]) -> int:
    seen = {}
    is_first = True
    num_ops = 0
    while is_first or tuple(cells) not in seen:
        seen[tuple(cells)] = num_ops

        cells = single_rebalance(cells)

        num_ops += 1
        is_first = False
    return num_ops - seen[tuple(cells)]


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines += [line.strip()]
    print(rebalance([int(x) for x in lines[0].split()]))


class Tests062(unittest.TestCase):
    def test_1(self):
        self.assertEqual(single_rebalance([0, 2, 7, 0]), [2, 4, 1, 2])

    def test_2(self):
        self.assertEqual(single_rebalance([2, 4, 1, 2]), [3, 1, 2, 3])

    def test_3(self):
        self.assertEqual(single_rebalance([3, 1, 2, 3]), [0, 2, 3, 4])

    def test_4(self):
        self.assertEqual(single_rebalance([0, 2, 3, 4]), [1, 3, 4, 1])

    def test_5(self):
        self.assertEqual(single_rebalance([1, 3, 4, 1]), [2, 4, 1, 2])

    def test_6(self):
        self.assertEqual(rebalance([0, 2, 7, 0]), 4)
