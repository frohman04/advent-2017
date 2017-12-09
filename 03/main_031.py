import fileinput
from typing import Generator, List, Tuple
import unittest


def neighbors(count: int) -> Generator[Tuple[int, List[int]], None, None]:
    """
    Calculate the neighbors for cell that have and index less than the cell's index.

    :param count: the number of neighbors to emit, starting with cell 1, going to cell n

    :return: (cell number, [neighbors])
    """
    idx = 1

    next_adj = 1
    length = 1
    curr = 0
    num_occurrances = 0
    skip_next = False
    for _ in range(count):
        if idx == 1:
            prev = []
        else:
            prev = [idx - 1]

        if idx < 4:
            adj = []
        elif curr < length:
            if curr > 0:
                next_adj += 1
            curr += 1
            if curr == length:
                skip_next = True
            adj = [next_adj]
        elif skip_next:
            adj = []
            skip_next = False
            curr = 0
            num_occurrances += 1
            if num_occurrances == 2:
                num_occurrances = 0
                length += 1
        else:
            raise Exception('Unexpected state')

        yield (idx, prev + adj)

        idx += 1


def dist(idx: int) -> int:
    """
    Calculate the Manhattan distance from a cell to cell 0 on a spiral grid.

    :param idx: the cell number of the cell to get the distance for

    :return: the Manhattan distance
    """
    dists = [-1] * (idx + 1)
    for idx, ns in neighbors(idx):
        if len(ns) == 0:
            dists[idx] = 0
        else:
            dists[idx] = min(dists[x] for x in ns) + 1
    return dists[idx]


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines += [line.strip()]
    print(dist(int(lines[0])))


class Tests031(unittest.TestCase):
    def test_neighbors(self):
        ns = [x for x in neighbors(16)]
        self.assertEqual([
            (1, []),
            (2, [1]),
            (3, [2]),
            (4, [3, 1]),
            (5, [4]),
            (6, [5, 1]),
            (7, [6]),
            (8, [7, 1]),
            (9, [8, 2]),
            (10, [9]),
            (11, [10, 2]),
            (12, [11, 3]),
            (13, [12]),
            (14, [13, 3]),
            (15, [14, 4]),
            (16, [15, 5])
        ], ns)

    def test_1(self):
        self.assertEqual(0, dist(1))

    def test_2(self):
        self.assertEqual(3, dist(12))

    def test_3(self):
        self.assertEqual(2, dist(23))

    def test_4(self):
        self.assertEqual(31, dist(1024))
