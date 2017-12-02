import fileinput
from typing import List
import unittest


def checksum(data: List[List[int]]) -> int:
    running_sum = 0
    for line in data:
        running_sum += (max(line) - min(line))
    return running_sum


def parse(data_str: List[str]) -> List[List[int]]:
    data = []  # type: List[List[int]]
    for line in data_str:
        data += [[int(x) for x in line.split()]]
    return data


if __name__ == '__main__':
    lines = []
    for line in fileinput.input():
        lines += [line]
    print(checksum(parse(lines)))


class Tests(unittest.TestCase):
    def test_1(self):
        self.assertEqual(18, checksum(parse(['5 1 9 5', '7 5 3', '2 4 6 8'])))
