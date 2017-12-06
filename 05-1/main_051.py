import fileinput
from typing import List
import unittest


def do_jumps(jumps: List[int]) -> int:
    count = 0
    i = 0
    while i < len(jumps):
        dist = jumps[i]
        jumps[i] += 1
        i += dist
        count += 1
    return count


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines += [line.strip()]
    print(do_jumps([int(x) for x in lines]))


class Tests051(unittest.TestCase):
    def test_1(self):
        self.assertEqual(do_jumps([0, 3, 0, 1, -3]), 5)
